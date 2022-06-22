import os
import psycopg2
from app.shop_units.dao import PostgresDAO
from app.exceptions import ValidationError, NotFoundError
import pytest
from app.dto import ShopUnitImport
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(
    host=os.environ["host"],
    user=os.environ["username"],
    password=os.environ["password"],
    database=os.environ["db_name"]
)
dao = PostgresDAO(conn, "shop_units")


def test_not_found_delete():
    with pytest.raises(NotFoundError):
        dao.delete_item("3aa85f64-5717-4562-b3fc-2c963f66a333")


def test_not_found_get():
    with pytest.raises(NotFoundError):
        dao.get_item("3aa85f64-5717-4562-b3fc-2c963f66a333")


# проверка того что мы не можем сменить тип товара при обновлении
@pytest.mark.parametrize("old_unit_type, old_price, new_unit_type, new_price",
                         [("OFFER", 5, "CATEGORY", None)])
def test_validation_error_in_update(old_unit_type, old_price, new_unit_type, new_price):
    unit_old_1 = ShopUnitImport(id="3fa85f64-5717-4562-b3fc-2c963f66a666", name="old", parentId=None, price=old_price,
                                type=old_unit_type)
    unit_new_1 = ShopUnitImport(id="3fa85f64-5717-4562-b3fc-2c963f66a666", name="new", parentId=None, price=new_price,
                                type=new_unit_type)
    update_date = "2022-05-28T21:12:01.000Z"
    with pytest.raises(ValidationError):
        dao.insert_or_update_items([unit_old_1], update_date)
        dao.insert_or_update_items([unit_new_1], update_date)
        dao.delete_item(unit_new_1.id)
        dao.delete_item(unit_old_1.id)
    dao.delete_item("3fa85f64-5717-4562-b3fc-2c963f66a666")


def test_get_item():
    unit_1 = ShopUnitImport(id="3aa85f64-5717-4562-b3fc-2c963f66a111", name="1", parentId=None, price=None,
                            type="CATEGORY")
    unit_2 = ShopUnitImport(id="3aa85f64-5717-4562-b3fc-2c963f66a222", name="2",
                            parentId="3aa85f64-5717-4562-b3fc-2c963f66a111",
                            price=None, type="CATEGORY")
    unit_3 = ShopUnitImport(id="3aa85f64-5717-4562-b3fc-2c963f66a333", name="3",
                            parentId="3aa85f64-5717-4562-b3fc-2c963f66a111",
                            price=None, type="CATEGORY")
    unit_4 = ShopUnitImport(id="3aa85f64-5717-4562-b3fc-2c963f66a444", name="4",
                            parentId="3aa85f64-5717-4562-b3fc-2c963f66a222",
                            price=None, type="CATEGORY")
    unit_5 = ShopUnitImport(id="3aa85f64-5717-4562-b3fc-2c963f66a555", name="5",
                            parentId="3aa85f64-5717-4562-b3fc-2c963f66a222",
                            price=None, type="CATEGORY")
    unit_6 = ShopUnitImport(id="3aa85f64-5717-4562-b3fc-2c963f66a666", name="6",
                            parentId="3aa85f64-5717-4562-b3fc-2c963f66a333",
                            price=None, type="CATEGORY")
    unit_7 = ShopUnitImport(id="3aa85f64-5717-4562-b3fc-2c963f66a777", name="7",
                            parentId="3aa85f64-5717-4562-b3fc-2c963f66a333",
                            price=None, type="CATEGORY")
    unit_8 = ShopUnitImport(id="3aa85f64-5717-4562-b3fc-2c963f66a888", name="8",
                            parentId="3aa85f64-5717-4562-b3fc-2c963f66a444",
                            price=None, type="CATEGORY")
    unit_9 = ShopUnitImport(id="3aa85f64-5717-4562-b3fc-2c963f66a999", name="9",
                            parentId="3aa85f64-5717-4562-b3fc-2c963f66a555",
                            price=None, type="CATEGORY")
    unit_10 = ShopUnitImport(id="3ba85f64-5717-4562-b3fc-2c963f66a111", name="10",
                             parentId="3aa85f64-5717-4562-b3fc-2c963f66a666", price=None, type="CATEGORY")
    update_date = "2022-05-28T21:12:01.011Z"
    dao.insert_or_update_items([unit_1, unit_2, unit_3, unit_4, unit_5, unit_6, unit_7, unit_8, unit_9, unit_10],
                               update_date)
    item_response = dao.get_item(unit_1.id)
    dao.delete_item("3aa85f64-5717-4562-b3fc-2c963f66a111")
    assert len(item_response.children) == 2


@pytest.mark.parametrize("delete_id",
                         ["3aa85f64-5717-4562-b3fc-2c963f66a222",
                          "3aa85f64-5717-4562-b3fc-2c963f66a333", "3aa85f64-5717-4562-b3fc-2c963f66a444",
                          "3aa85f64-5717-4562-b3fc-2c963f66a555", "3aa85f64-5717-4562-b3fc-2c963f66a666",
                          "3aa85f64-5717-4562-b3fc-2c963f66a777", "3aa85f64-5717-4562-b3fc-2c963f66a888",
                          "3aa85f64-5717-4562-b3fc-2c963f66a888", "3aa85f64-5717-4562-b3fc-2c963f66a999",
                          "3ba85f64-5717-4562-b3fc-2c963f66a111"])
def test_delete_item(delete_id):
    with pytest.raises(NotFoundError):
        dao.delete_item(delete_id)
