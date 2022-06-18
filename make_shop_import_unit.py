from typing import Optional, List
from dto import ShopUnitType, ShopUnitImport


def make_shop_import_unit(unit_id: str, name: str, parent_id: Optional[str], price: Optional[int],
                          unit_type: str) -> ShopUnitImport:
    unit = ShopUnitImport()
    unit.id = unit_id
    unit.name = name
    unit.parentId = parent_id
    unit.price = price
    unit.type = unit_type
    return unit
