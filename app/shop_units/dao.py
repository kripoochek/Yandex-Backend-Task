from datetime import datetime
from typing import List, Dict, Protocol, Tuple
from uuid import UUID
from app.dto import ShopUnitImport, ShopUnit, ShopUnitType
from app.exceptions import ValidationError, NotFoundError
import psycopg2.extras

psycopg2.extras.register_uuid()

start_script = """create type unit_type AS ENUM ('OFFER', 'CATEGORY');
create table if not exists public.shop_units (
id UUID not null,
name text not null,
parent_id UUID null,
price int null,
type unit_type,
update_date timestamp without time zone ,
primary key(id)
);
alter table public.shop_units add constraint fk_parent_category foreign key(parent_id) references shop_units(id) on delete cascade;
-- trigger to prevent changing shop unit type.
create or replace function prevent_type_change() returns trigger as $prevent_type_change$
begin
  if old.type != new.type then
    raise exception 'change type is not allowed';
  end if;

  if old.type = 'OFFER' and new.price is null then
    raise exception 'offer must have price';
  end if;

  if old.type = 'CATEGORY' and new.price is not null then
    raise exception 'category must have null price';
  end if;
  if old.type = 'OFFER' and new.price<0 then
    raise exception 'OFFER price must be positiv';
  end if;
  return new;
end;
$prevent_type_change$ language plpgsql;

create trigger prevent_type_change before update on public.shop_units
for each row execute procedure prevent_type_change();
create table if not exists public.statistic_shop_units (
id UUID not null,
name text not null,
parent_id UUID null,
price int null,
type unit_type,
update_date timestamp without time zone
);
alter table public.statistic_shop_units add constraint fk_statistic foreign key(id) references shop_units(id) on delete cascade;
"""


def item_to_unit(item: tuple, children: Dict[UUID, tuple]) -> ShopUnit:
    dt_str = item[5].strftime("%Y-%m-%dT%H:%M:%S.000Z")
    unit = ShopUnit(id=item[0], name=item[1], parentId=item[2], price=item[3], type=item[4], date=dt_str)
    if item[0] in children:
        unit.children = list()
        for child in children[item[0]]:
            unit.children.append(item_to_unit(child, children))
    else:
        unit.children = None
    return unit


def making_list_children(items: list):
    dict_of_children = dict()
    for i in range(len(items)):
        item = items[i]
        if item[2] is not None:
            if item[2] not in dict_of_children:
                dict_of_children[item[2]] = list()
                dict_of_children[item[2]].append(item)
            else:
                dict_of_children[item[2]].append(item)
    unit = item_to_unit(items[0], dict_of_children)
    return unit


class DAO(Protocol):
    """
        DAO represents interface with set of methods to work with shop units storage.
    """

    def insert_or_update_items(self, items: List["ShopUnitImport"], update_date: datetime) -> None:
        """
        Inserts or updates provided items and updates their update time
        :param items: shop units import data
        :param update_date: update time
        :return:
        """
        pass

    def get_item(self, item_id: UUID) -> ShopUnit:
        """
        Deletes item and its children recursively.
        :param item_id: uuid shop unit
        :return:
        """
        pass

    def delete_item(self, item_id: UUID):
        """
        Deletes item and its children recursively.
        :param item_id uuid shop unit
        :return:
        """
        pass

    def get_sales(self, date: datetime):
        """
        Get items
        """
        pass

    def get_statistic(self, item_id: UUID, date_start: datetime, date_end: datetime):
        """
        Get statistic between dateStart and dateEnd
        """
        pass


class PostgresDAO:
    def __init__(self, conn, table_name: str):
        self._conn = conn
        self._table_name = table_name
        self._script = start_script
        with self._conn.cursor() as cursor:
            cursor.execute(self._script)

    def __del__(self):
        if self._conn:
            self._conn.close()

    def insert_or_update_items(self, items: List[ShopUnitImport], update_date: datetime):
        try:
            with self._conn.cursor() as cursor:
                for item in items:
                    if item.parent_id is not None:
                        cursor.execute(
                            """
                                select type from shop_units where id = %s;
                            """,
                            (item.parent_id,)
                        )
                        parent_type = cursor.fetchall()
                        if len(parent_type) == 0:
                            raise ValidationError
                        if parent_type[0][0] == ShopUnitType.OFFER:
                            raise ValidationError
                    cursor.execute(
                        """
                        insert into shop_units(id, name, parent_id, price, type, update_date)
                        values(%s, %s, %s, %s, %s, %s)
                        on conflict (id)
                        do update set name = %s, parent_id = %s, price = %s, type = %s, update_date = %s;
                        """,
                        (
                            item.id, item.name, item.parent_id, item.price, item.type, update_date,
                            item.name, item.parent_id, item.price, item.type, update_date)
                    )
                    cursor.execute(
                        """
                        SELECT * FROM information_schema.tables;;
                        """
                    )
                    cursor.execute(
                        """
                         insert into statistic_shop_units(id, name, parent_id, price, type, update_date)
                        values(%s, %s, %s, %s, %s, %s)
                        """, (item.id, item.name, item.parent_id, item.price, item.type, update_date)
                    )
                    cursor.execute(
                        """
                        update shop_units x set update_date = %s from (
                        with recursive tree as (
                        select su.id, su.name, su.parent_id, su.price, su.type, su.update_date  from shop_units  su
                        where su.id = %s
                        union all
                        select parent.id, parent.name, parent.parent_id, parent.price, parent.type, parent.update_date 
                        from shop_units parent, tree
                         where parent.id = tree.parent_id
                        ) select id from tree
                        ) as parents where x.id = parents.id;
                        """,
                        (
                            update_date, item.id
                        )
                    )
                    self._conn.commit()
        except BaseException:
            self._conn.rollback()
            raise ValidationError

    def get_item(self, item_id: UUID) -> ShopUnit:
        with self._conn.cursor() as cursor:
            cursor.execute(
                """
                with recursive tree as (
                select su.id, su.name, su.parent_id, su.price, su.type, su.update_date  from shop_units su
                where su.id = %s
    
                union all
    
                select child.id, child.name, child.parent_id, child.price, child.type, child.update_date from shop_units child, tree
                where child.parent_id = tree.id
                ) select * from tree;
                """,
                (item_id,)
            )
            items = list(cursor.fetchall())
            if len(items) == 0:
                raise NotFoundError
            return making_list_children(items)

    def delete_item(self, item_id: UUID):
        with self._conn.cursor() as cursor:
            cursor.execute(
                """
                delete from shop_units where id = %s returning id ;
                """,
                (item_id,)
            )
            if len(cursor.fetchall()) == 0:
                raise NotFoundError
            self._conn.commit()

    def get_sales(self, date: datetime) -> List[Tuple]:
        with self._conn.cursor() as cursor:
            cursor.execute(
                """
                select * from shop_units su where (su.type='OFFER' and 
                ((DATE_PART('day', %s::timestamp - su.update_date::timestamp) * 24 + 
                DATE_PART('hour', %s::timestamp - su.update_date::timestamp)) * 60 +
                DATE_PART('minute', %s::timestamp - su.update_date::timestamp)) * 60 +
                DATE_PART('second', %s::timestamp - su.update_date::timestamp)<=86400 and 
                ((DATE_PART('day', %s::timestamp - su.update_date::timestamp) * 24 + 
                DATE_PART('hour', %s::timestamp - su.update_date::timestamp)) * 60 +
                DATE_PART('minute', %s::timestamp - su.update_date::timestamp)) * 60 +
                DATE_PART('second', %s::timestamp - su.update_date::timestamp)>=0);
                """
                , (date, date, date, date, date, date, date, date)
            )
            return list(cursor.fetchall())

    def get_statistic(self, item_id: UUID, date_start: datetime, date_end: datetime) -> List[Tuple]:
        with self._conn.cursor() as cursor:
            cursor.execute(
                """select * from statistic_shop_units su where (su.id=%s and su.update_date>=%s and 
                su.update_date<=%s); """, (item_id, date_start, date_end)
            )
            if len(cursor.fetchall()) == 0:
                raise NotFoundError
            return list(cursor.fetchall())
