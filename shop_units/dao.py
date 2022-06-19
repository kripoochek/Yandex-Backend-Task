from datetime import datetime
from typing import List, Dict, Protocol
from uuid import UUID

import psycopg2
from dto import ShopUnitImport, ShopUnit
from config import host, user, password, db_name
from exceptions import ValidationError, NotFoundError
import psycopg2.extras

psycopg2.extras.register_uuid()


def item_to_unit(item: tuple, children: Dict[UUID, tuple]) -> ShopUnit:
    unit = ShopUnit(id=item[0], name=item[1], parentId=item[2], price=item[3], type=item[4], date=item[5])
    if item[0] in children:
        unit.children = list()
        for child in children[item[0]]:
            unit.children.append(item_to_unit(child, children))
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

    def insert_or_update_nodes(self, items: List["ShopUnitImport"], update_date: datetime) -> None:
        """
        Inserts or updates provided items and updates their update time
        :param items: shop units import data
        :param update_date: update time
        :return:
        """
        pass

    def get_node(self, item_id: UUID) -> ShopUnit:
        """
        Deletes node and its children recursively.
        :param item_id: uuid shop unit
        :return:
        """
        pass

    def delete_node(self, item_id: UUID):
        """
        Deletes node and its children recursively.
        :param item_id uuid shop unit
        :return:
        """
        pass


class PostgresDAO:
    def __init__(self, conn, table_name: str):
        self._conn = conn
        self._table_name = table_name

    def __del__(self):
        if self._conn:
            self._conn.close()

    def insert_or_update_nodes(self, items: List[ShopUnitImport], update_date: datetime):
        try:
            with self._conn.cursor() as cursor:
                for item in items:
                    if item.parent_id is not None:
                        cursor.execute(
                            """
                                select * from shop_units where id = %s;
                            """,
                            (item.parent_id,)
                        )
                        if cursor.fetchone()[4] == "OFFER":
                            raise ValidationError
                    cursor.execute(
                        """
                        insert into %s(id, name, parent_id, price, type, update_date)
                        values(%s, %s, %s, %s, %s, %s)
                        on conflict (id)
                        do update set name = %s, parent_id = %s, price = %s, type = %s, update_date = %s;
                        """,
                        (
                            self._table_name, item.id, item.name, item.parent_id, item.price, item.type, update_date,
                            item.name, item.parent_id, item.price, item.type, update_date)
                    )
                    self._conn.commit()
        except ValidationError:
            self._conn.rollback()
            raise ValidationError

    def get_node(self, item_id: UUID) -> ShopUnit:
        with self._conn.cursor() as cursor:
            cursor.execute(
                """
                with recursive tree as (
                select su.id, su.name, su.parent_id, su.price, su.type, su.update_date  from %s su
                where su.id = %s
    
                union all
    
                select child.id, child.name, child.parent_id, child.price, child.type, child.update_date from shop_units child, tree
                where child.parent_id = tree.id
                ) select * from tree;
                """,
                (self._table_name, item_id,)
            )
            items = list(cursor.fetchall())
            if len(items) == 0:
                raise ValidationError
            return making_list_children(items)

    def delete_node(self, item_id: UUID):
        with self._conn.cursor() as cursor:
            cursor.execute(
                """
                delete from %s where id = %s returning id ;
                """,
                (self._table_name, item_id,)
            )
            if len(cursor.fetchall()) == 0:
                raise NotFoundError
            self._conn.commit()
