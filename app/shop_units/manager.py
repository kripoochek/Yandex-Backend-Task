import json
from datetime import datetime
from typing import List, Tuple, Optional, Protocol, Dict
from uuid import UUID
from app.exceptions import ValidationError
from app.shop_units.dao import DAO
from app.dto import ShopUnitImport, ShopUnit, ShopUnitType


def dfs(item: ShopUnitImport, graph: Dict[UUID, List[ShopUnit]], out_time_order: List[UUID], used: Dict[UUID, bool]):
    if item.id in used:
        return
    used[item.id] = True
    if item.id in graph:
        for child in graph[item.id]:
            dfs(child, graph, out_time_order, used)
    out_time_order.append(item)


def right_order_items(items: List[ShopUnitImport], graph: Dict[UUID, List[ShopUnit]]):
    used = dict()
    out_time_order = list()
    for item in items:
        if item.id in used:
            continue
        dfs(item, graph, out_time_order, used)
    return reversed(out_time_order)


def price(unit: ShopUnit) -> Optional[int]:
    if unit.type == ShopUnitType.OFFER:
        return unit.price
    if unit.children is None:
        return None

    def f(u: ShopUnit) -> Tuple[int, int]:
        """
        calculate the total price and count them in the category
        """
        if u.type == ShopUnitType.CATEGORY:
            total_price, cnt = 0, 0
            if u.children is not None:
                for child in u.children:
                    a, b = f(child)
                    total_price += a
                    cnt += b
            if cnt == 0:
                u.price = None
            else:
                u.price = total_price // cnt
            return total_price, cnt
        if u.type == ShopUnitType.OFFER:
            return u.price, 1

    s, count = f(unit)
    if count == 0:
        return None
    return s // count


class ManagerInterface(Protocol):
    def __init__(self, dao: DAO):
        pass

    def delete_item(self, item_id: str):
        pass

    def get_item(self, item_id: str) -> str:
        pass

    def import_items(self, items: List[ShopUnitImport], update_date: str):
        pass

    def get_sales(self, date: datetime) -> List[ShopUnit]:
        pass


class Manager:
    def __init__(self, dao: DAO):
        # print("MANAGER")

        self.dao = dao

    def import_items(self, items: List[ShopUnitImport], update_date: datetime) -> None:
        id_to_item = dict()  # Dict[UUID, ShopUnit]
        graph = dict()  # Dict[UUID, List[ShopUnit]]
        for item in items:
            if item.id not in id_to_item:
                id_to_item[item.id] = item
            else:
                raise ValidationError
            if item.parent_id is not None:
                if item.parent_id not in graph:
                    graph[item.parent_id] = list()
                    graph[item.parent_id].append(item)
                else:
                    graph[item.parent_id].append(item)
        items = right_order_items(items, graph)
        self.dao.insert_or_update_items(items, update_date)

    def get_item(self, item_id: UUID) -> ShopUnit:
        shop_unit = self.dao.get_item(item_id)
        shop_unit.price = price(shop_unit)
        return json.loads(shop_unit.json())

    def delete_item(self, item_id: UUID) -> None:
        self.dao.delete_item(item_id)

    def get_sales(self, date: datetime) -> List[ShopUnit]:
        items = self.dao.get_sales(date)
        for i in range(len(items)):
            dt_str = items[i][5].strftime("%Y-%m-%dT%H:%M:%S.000Z")
            items[i] = ShopUnit(id=items[i][0], name=items[i][1], parentId=items[i][2], price=items[i][3],
                                type=items[i][4],
                                date=dt_str)
            items[i] = json.loads(items[i].json())
        return items
