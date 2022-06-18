from dto import ShopUnit
from shop_units.postgres_dao import PostgresDAO
from typing import Protocol, List


class DAO(Protocol):
    def insert_or_update(self, items: List["ShopUnitImport"], update_date: str):
        pass

    def get_item(self, item_id: str) -> ShopUnit:
        pass

    def delete_item(self, item_id: str):
        pass
