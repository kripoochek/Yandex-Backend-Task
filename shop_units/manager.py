from datetime import datetime
from typing import List, Dict, Union
from uuid import UUID
from exceptions import NotFoundError, ValidationError
from shop_units.dao import DAO
from dto import ShopUnitImport, ShopUnit


def is_datetime_valid(dt_str):
    try:
        dt_str_new = dt_str.replace('Z', '+00:00')
        datetime.fromisoformat(dt_str_new)
    except:
        return False
    return True


def is_valid_uuid(value):
    try:
        UUID(value)

        return True
    except ValueError:
        return False


def price_counter(unit: Union["ShopUnit", "ShopUnitChildren"]):
    if unit.price is not None:
        return
    if not hasattr(unit, "children"):
        return
    count_children_with_price = 0
    sum_price = 0
    for i in range(len(unit.children)):
        price_counter(unit.children[i])
        if unit.children[i].price is not None:
            count_children_with_price += 1
            sum_price += unit.children[i].price
    if count_children_with_price != 0:
        unit.price = sum_price


def make_children_dict(children: List["ShopUnit"]):
    for i in range(len(children)):
        if hasattr(children[i], "children"):
            pass


class Manager:
    def __init__(self, dao: DAO):
        print("initialize manager")
        self.dao = dao

    def import_nodes(self, items: List["ShopUnitImport"], update_date: str):
        items_id = dict()
        for item in items:
            if item.id not in items_id:
                items_id[item.id] = 1
            else:
                items_id[item.id] += 1
            if items_id[item.id] > 1:
                raise ValidationError
            if not is_valid_uuid(item.id):
                raise ValidationError
            if item.parentId is not None:
                if not is_valid_uuid(item.parentId):
                    raise ValidationError
            if item.type == "CATEGORY" and item.price is not None:
                raise ValidationError
            if item.type == "OFFER" and (item.price is None or item.price < 0):
                raise ValidationError
            if item.type != "OFFER" and item.type != "CATEGORY":
                raise ValidationError
            if not is_datetime_valid(update_date):
                raise ValidationError
        self.dao.insert_or_update(items, update_date)

    def get_node(self, item_id: str) -> ShopUnit:
        if not is_valid_uuid(item_id):
            raise ValidationError
        shop_unit = self.dao.get_item(item_id)
        price_counter(shop_unit)
        return shop_unit

    def delete_node(self, item_id: str):
        if not is_valid_uuid(item_id):
            raise ValidationError
        self.dao.delete_item(item_id)
