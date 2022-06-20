from app.shop_units.dao import PostgresDAO
from make_shop_import_unit import make_shop_import_unit
from app.exceptions import ValidationError, NotFoundError
import pytest

dao = PostgresDAO()


def test_not_found_delete():
    with pytest.raises(NotFoundError):
        dao.delete_item("3fa85f64-5717-4562-b3fc-2c963f66a333")


def test_not_found_get():
    with pytest.raises(NotFoundError):
        dao.get_item("3fa85f64-5717-4562-b3fc-2c963f66a333")


@pytest.mark.parametrize("old_unit_type, old_price, new_unit_type, new_price",
                         [("OFFER", 5, "CATEGORY", None), ("OFFER", 5, "OFFER", None),
                          ("CATEGORY", None, "CATEGORY", 5), ("OFFER", 5, "OFFER", -5)])
def test_validation_error_in_update(old_unit_type, old_price, new_unit_type, new_price):
    unit_old_1 = make_shop_import_unit("3fa85f64-5717-4562-b3fc-2c963f66a666", "old", None, old_price, old_unit_type)
    unit_new_1 = make_shop_import_unit("3fa85f64-5717-4562-b3fc-2c963f66a666", "new", None, new_price, new_unit_type)
    update_date = "2022-05-28T21:12:01.000Z"
    with pytest.raises(ValidationError):
        dao.insert_or_update([unit_old_1], update_date)
        dao.insert_or_update([unit_new_1], update_date)
        dao.delete_item(unit_new_1.id)
        dao.delete_item(unit_old_1.id)


def test_get_item():
    unit_1 = make_shop_import_unit("3aa85f64-5717-4562-b3fc-2c963f66a111", "1", None, None, "CATEGORY")
    unit_2 = make_shop_import_unit("3aa85f64-5717-4562-b3fc-2c963f66a222", "2", "3aa85f64-5717-4562-b3fc-2c963f66a111",
                                   None, "CATEGORY")
    unit_3 = make_shop_import_unit("3aa85f64-5717-4562-b3fc-2c963f66a333", "3", "3aa85f64-5717-4562-b3fc-2c963f66a111",
                                   None, "CATEGORY")
    unit_4 = make_shop_import_unit("3aa85f64-5717-4562-b3fc-2c963f66a444", "4", "3aa85f64-5717-4562-b3fc-2c963f66a222",
                                   None, "CATEGORY")
    unit_5 = make_shop_import_unit("3aa85f64-5717-4562-b3fc-2c963f66a555", "5", "3aa85f64-5717-4562-b3fc-2c963f66a222",
                                   None, "CATEGORY")
    unit_6 = make_shop_import_unit("3aa85f64-5717-4562-b3fc-2c963f66a666", "6", "3aa85f64-5717-4562-b3fc-2c963f66a333",
                                   None, "CATEGORY")
    unit_7 = make_shop_import_unit("3aa85f64-5717-4562-b3fc-2c963f66a777", "7", "3aa85f64-5717-4562-b3fc-2c963f66a333",
                                   None, "CATEGORY")
    unit_8 = make_shop_import_unit("3aa85f64-5717-4562-b3fc-2c963f66a888", "8", "3aa85f64-5717-4562-b3fc-2c963f66a444",
                                   None, "CATEGORY")
    unit_9 = make_shop_import_unit("3aa85f64-5717-4562-b3fc-2c963f66a999", "9", "3aa85f64-5717-4562-b3fc-2c963f66a555",
                                   None, "CATEGORY")
    unit_10 = make_shop_import_unit("3ba85f64-5717-4562-b3fc-2c963f66a111", "10",
                                    "3aa85f64-5717-4562-b3fc-2c963f66a666", None, "CATEGORY")
    update_date = "2022-05-28T21:12:01.011Z"
    dao.insert_or_update([unit_1, unit_2, unit_3, unit_4, unit_5, unit_6, unit_7, unit_8, unit_9, unit_10], update_date)
    item_response = dao.get_item(unit_1.id)
    assert len(item_response.children) == 2


@pytest.mark.parametrize("delete_id",
                         ["3aa85f64-5717-4562-b3fc-2c963f66a111", "3aa85f64-5717-4562-b3fc-2c963f66a222",
                          "3aa85f64-5717-4562-b3fc-2c963f66a333", "3aa85f64-5717-4562-b3fc-2c963f66a444",
                          "3aa85f64-5717-4562-b3fc-2c963f66a555", "3aa85f64-5717-4562-b3fc-2c963f66a666",
                          "3aa85f64-5717-4562-b3fc-2c963f66a777", "3aa85f64-5717-4562-b3fc-2c963f66a888",
                          "3aa85f64-5717-4562-b3fc-2c963f66a888", "3aa85f64-5717-4562-b3fc-2c963f66a999",
                          "3ba85f64-5717-4562-b3fc-2c963f66a111"])
def test_delete_item(delete_id):
    unit_1 = make_shop_import_unit("3aa85f64-5717-4562-b3fc-2c963f66a111", "1", None, None, "CATEGORY")
    unit_2 = make_shop_import_unit("3aa85f64-5717-4562-b3fc-2c963f66a222", "2", "3aa85f64-5717-4562-b3fc-2c963f66a111",
                                   None, "CATEGORY")
    unit_3 = make_shop_import_unit("3aa85f64-5717-4562-b3fc-2c963f66a333", "3", "3aa85f64-5717-4562-b3fc-2c963f66a111",
                                   None, "CATEGORY")
    unit_4 = make_shop_import_unit("3aa85f64-5717-4562-b3fc-2c963f66a444", "4", "3aa85f64-5717-4562-b3fc-2c963f66a222",
                                   None, "CATEGORY")
    unit_5 = make_shop_import_unit("3aa85f64-5717-4562-b3fc-2c963f66a555", "5", "3aa85f64-5717-4562-b3fc-2c963f66a222",
                                   None, "CATEGORY")
    unit_6 = make_shop_import_unit("3aa85f64-5717-4562-b3fc-2c963f66a666", "6", "3aa85f64-5717-4562-b3fc-2c963f66a333",
                                   None, "CATEGORY")
    unit_7 = make_shop_import_unit("3aa85f64-5717-4562-b3fc-2c963f66a777", "7", "3aa85f64-5717-4562-b3fc-2c963f66a333",
                                   None, "CATEGORY")
    unit_8 = make_shop_import_unit("3aa85f64-5717-4562-b3fc-2c963f66a888", "8", "3aa85f64-5717-4562-b3fc-2c963f66a444",
                                   None, "CATEGORY")
    unit_9 = make_shop_import_unit("3aa85f64-5717-4562-b3fc-2c963f66a999", "9", "3aa85f64-5717-4562-b3fc-2c963f66a555",
                                   None, "CATEGORY")
    unit_10 = make_shop_import_unit("3ba85f64-5717-4562-b3fc-2c963f66a111", "10",
                                    "3aa85f64-5717-4562-b3fc-2c963f66a666", None, "CATEGORY")
    update_date = "2022-05-28T21:12:01.000Z"
    dao.insert_or_update([unit_1, unit_2, unit_3, unit_4, unit_5, unit_6, unit_7, unit_8, unit_9, unit_10], update_date)
    dao.delete_item(unit_1.id)
    with pytest.raises(NotFoundError):
        dao.delete_item(delete_id)
