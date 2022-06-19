from datetime import datetime
from typing import List, Dict, Union, Tuple, Optional, Protocol
from uuid import UUID
from exceptions import NotFoundError, ValidationError
from shop_units.dao import DAO
from dto import ShopUnitImport, ShopUnit, ShopUnitType


def price(unit: ShopUnit) -> Optional[int]:
    if unit.type == ShopUnitType.OFFER:
        return unit.price
    if unit.children is None:
        return None

    def f(u: ShopUnit) -> Tuple[int, int]:
        if u.type == ShopUnitType.CATEGORY:
            total_price, cnt = 0, 0
            for child in u.children:
                a, b = f(child)
                total_price += a
                cnt += b
            u.price = total_price // (cnt if cnt != 0 else 1)
            return total_price, cnt
        if u.type == ShopUnitType.OFFER:
            return u.price, 1

    s, count = f(unit)
    return s // (count if count != 0 else 1)


class ManagerInterface(Protocol):
    def __init__(self, dao: DAO):
        pass

    def delete_node(self, item_id: str):
        pass

    def get_node(self, item_id: str) -> str:
        pass

    def import_nodes(self, items: List[ShopUnitImport], update_date: str):
        pass


class Manager:
    def __init__(self, dao: DAO):
        self.dao = dao

    def import_nodes(self, items: List[ShopUnitImport], update_date: datetime) -> None:
        items_id = dict()
        for item in items:
            if item.id not in items_id:
                items_id[item.id] = 1
            else:
                items_id[item.id] += 1
            if items_id[item.id] > 1:
                raise ValidationError
        self.dao.insert_or_update_nodes(items, update_date)

    def get_node(self, item_id: UUID) -> ShopUnit:
        shop_unit = self.dao.get_node(item_id)
        price(shop_unit)
        return shop_unit

    def delete_node(self, item_id: UUID) -> None:
        self.dao.delete_node(item_id)
