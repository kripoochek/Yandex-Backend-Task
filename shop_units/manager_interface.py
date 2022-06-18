from typing import Protocol, List
from shop_units.dao import DAO


class ManagerInterface(Protocol):
    def __init__(self, dao: DAO):
        pass

    def delete_node(self, item_id: str):
        pass

    def get_node(self, item_id: str) -> str:
        pass

    def import_nodes(self, items: List["ShopUnitImport"], update_date: str):
        pass
