from datetime import datetime
from time import strftime
from typing import List
import psycopg2
from dto import ShopUnitImport, ShopUnitType, ShopUnit
from config import host, user, password, db_name
from exceptions import ValidationError, NotFoundError


def item_to_unit(item: tuple, dict_of_children: dict) -> ShopUnit:
    dt_str = item[5].strftime("%Y-%m-%dT%H:%M:%S.000Z")
    unit = ShopUnit(id=item[0], name=item[1], parentId=item[2], price=item[3], type=item[4], date=dt_str)
    if item[0] in dict_of_children:
        unit.children = list()
        for child in dict_of_children[item[0]]:
            unit.children.append(item_to_unit(child, dict_of_children))
    return unit


def making_list_children(items: list):
    id_to_pos = dict()
    dict_of_children = dict()
    for i in range(len(items)):
        item = items[i]
        id_to_pos[item[0]] = i
        if item[2] is not None:
            if item[2] not in dict_of_children:
                dict_of_children[item[2]] = list()
                dict_of_children[item[2]].append(item)
            else:
                dict_of_children[item[2]].append(item)
    unit = item_to_unit(items[0], dict_of_children)
    return unit


class PostgresDAO:
    def __init__(self):
        print("initialize dao")
        self.conn = None
        try:
            self.conn = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
        except psycopg2.DatabaseError as error:
            # print(error)
            raise error

    def __del__(self):
        if self.conn:
            self.conn.close()

    def insert_or_update(self, items: List["ShopUnitImport"], update_date: str):
        try:
            with self.conn.cursor() as cursor:
                for item in items:
                    if item.parentId is not None:
                        cursor.execute(
                            """
                            select * from shop_units where id = %s;
                            """,
                            (item.parentId,)
                        )
                        if cursor.fetchone()[4] == "OFFER":
                            raise ValidationError
                    cursor.execute(
                        """
                        insert into shop_units(id, name, parent_id, price, type, update_date)
                        values(%s, %s, %s, %s, %s, %s)
                        on conflict (id)
                        do update set name = %s, parent_id = %s, price = %s, type = %s, update_date = %s;
                        """,
                        (
                            item.id, item.name, item.parentId, item.price, item.type, update_date, item.name,
                            item.parentId,
                            item.price, item.type, update_date)
                    )
        except Exception:
            self.conn.rollback()
            raise ValidationError
        self.conn.commit()

    def get_item(self, item_id: str) -> ShopUnit:
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                select exists(select 1 from shop_units where id = %s)
                """,
                (item_id,)
            )
            if not cursor.fetchone()[0]:
                self.conn.rollback()
                raise NotFoundError
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
            return making_list_children(items)

    def delete_item(self, item_id: str):

        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                delete from shop_units where id = %s returning id ;
                """,
                (item_id,)
            )
            if len(cursor.fetchall()) == 0:
                raise NotFoundError
            self.conn.commit()
