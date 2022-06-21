from app.shop_units.dao import PostgresDAO
from app.shop_units.manager import Manager
from app.exceptions import ValidationError
from app.dto import ShopUnitImport
import pytest

#postgres_dao = PostgresDAO()
#manager = Manager(postgres_dao)
"""
@pytest.mark.parametrize("unit_id, parent_id, name, unit_type, price",
                         [("3aa85f64-5717-4562-b3fc-2c963f66a111", None, "1", "OFFER", -5),
                          ("3aa85f64-5717-4562-b3fc-2c963f66a111", None, "1", "CATEGORY", -5),
                          ("3aa85f64-5717-4562-b3fc-3f66a111", None, "1", "Cfewff", None),
                          ("3aa85f64-5717-4562-b3fc-2c963f66a111", "dqwdqwdwqdqwdwqd", "1", "OFFER", -5),
                          ("3aa85f64-5717-4562-b3fc-2c963f66a111", "3aa85f64-5717-4562-b3fc-2c963f66a111", "1", "OFFER",
                           5)])
def test_import(unit_id, parent_id, name, unit_type, price):
    unit_1 = ShopUnitImport(id=unit_id, name=name, parent_id=parent_id, price=price, type=unit_type)
    update_date = "2022-05-28T21:12:01.000Z"
    with pytest.raises(ValidationError):
        manager.import_nodes([unit_1], update_date)



"""