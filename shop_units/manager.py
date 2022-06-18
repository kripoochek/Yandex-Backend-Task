from datetime import datetime
from typing import List
from uuid import UUID
from exceptions import NotFoundError, ValidationError
from shop_units.dao import DAO
from dto import ShopUnitImport, ShopUnit


def is_datetime_valid(dt_str):
    try:
        datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    except:
        return False
    return True


def is_valid_uuid(value):
    try:
        UUID(value)

        return True
    except ValueError:
        return False


def price_counter(unit: ShopUnit):
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
        unit.price = sum_price // count_children_with_price


def str_response_format_children(children: List["ShopUnit"], indent: str) -> str:
    children_str = """\n%s"children": [""" % indent
    for child in children:
        if child.parentId is not None:
            child.parentId = '"' + child.parentId + '"'
        children_str += """\n%s  {
%s    "name": "%s",
%s    "id": "%s",
%s    "price": %s,
%s    "date": "%s",
%s    "type": "%s",
%s    "parentId": %s""" % (
            indent, indent, child.name, indent, child.id, indent, child.price, indent, child.date, indent, child.type,
            indent, child.parentId)
        if hasattr(child, "children"):
            children_str += ","
            children_str += str_response_format_children(child.children, indent + "    ")
        children_str += "\n%s  }" % indent
        if child != children[len(children) - 1]:
            children_str += ","
    new_indent = indent[2:]
    children_str += "\n%s  ]" % new_indent
    return children_str


def str_response_format_unit(unit: ShopUnit) -> str:
    if unit.parentId is not None:
        unit.parentId = '"' + unit.parentId + '"'
    item_str = """{
  "id": "%s",
  "name": "%s",
  "type": "%s",
  "parentId": %s,
  "date": "%s",
  "price": %s""" % (unit.id, unit.name, unit.type, unit.parentId, unit.date, unit.price)
    if hasattr(unit, "children"):
        item_str += ","
        item_str += str_response_format_children(unit.children, "  ")
    item_str += "\n}"
    return item_str


class Manager:
    def __init__(self, dao: DAO):
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

    def get_node(self, item_id: str) -> str:
        if not is_valid_uuid(item_id):
            raise ValidationError
        shop_unit = self.dao.get_item(item_id)
        price_counter(shop_unit)
        return str_response_format_unit(shop_unit)

    def delete_node(self, item_id: str):
        if not is_valid_uuid(item_id):
            raise ValidationError
        self.dao.delete_item(item_id)
