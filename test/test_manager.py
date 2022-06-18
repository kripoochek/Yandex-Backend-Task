from shop_units.postgres_dao import PostgresDAO
from make_shop_import_unit import make_shop_import_unit
from shop_units.manager import Manager
from exceptions import ValidationError, NotFoundError
import pytest

postgres_dao = PostgresDAO()
manager = Manager(postgres_dao)
expected_str = """{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66a111",
  "name": "Категория",
  "type": "CATEGORY",
  "parentId": null,
  "date": "2022-05-28T21:12:01.000Z",
  "price": 6,
  "children": [
    {
      "name": "Оффер 1",
      "id": "3fa85f64-5717-4562-b3fc-2c963f66a222",
      "price": 4,
      "date": "2022-05-28T21:12:01.000Z",
      "type": "OFFER",
      "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a111"
    },
    {
      "name": "Подкатегория",
      "type": "CATEGORY",
      "id": "3fa85f64-5717-4562-b3fc-2c963f66a333",
      "date": "2022-05-26T21:12:01.000Z",
      "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a111",
      "price": 8,
      "children": [
        {
          "name": "Оффер 2",
          "id": "3fa85f64-5717-4562-b3fc-2c963f66a444",
          "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a333",
          "date": "2022-05-26T21:12:01.000Z",
          "price": 8,
          "type": "OFFER"
        }
      ]
    }
  ]
}"""
"""
postgres_dao = PostgresDAO()
manage = Manager(postgres_dao)
unit_1 = make_shop_import_unit("3bb85f64-5717-4562-b3fc-2c963f66a111", "1offer",
                               "3aa85f64-5717-4562-b3fc-2c963f66a999", 11, "OFFER")
unit_2 = make_shop_import_unit("3bb85f64-5717-4562-b3fc-2c963f66a222", "2offer",
                               "3aa85f64-5717-4562-b3fc-2c963f66a999", 12, "OFFER")
unit_3 = make_shop_import_unit("3bb85f64-5717-4562-b3fc-2c963f66a333", "3cat",
                               "3aa85f64-5717-4562-b3fc-2c963f66a999", None, "CATEGORY")
unit_4 = make_shop_import_unit("3bb85f64-5717-4562-b3fc-2c963f66a444", "4offer",
                               "3aa85f64-5717-4562-b3fc-2c963f66a666", 21, "OFFER")
unit_5 = make_shop_import_unit("3bb85f64-5717-4562-b3fc-2c963f66a555", "5offer",
                               "3aa85f64-5717-4562-b3fc-2c963f66a666", 1, "OFFER")
update_date = "2022-05-28T21:12:01.000Z"
manage.import_nodes([unit_1, unit_2, unit_3, unit_4, unit_5], update_date)
manage.delete_node("3aa85f64-5717-4562-b3fc-2c963f66a111")
"""


@pytest.mark.parametrize("unit_id, parent_id, name, unit_type, price",
                         [("3aa85f64-5717-4562-b3fc-2c963f66a111", None, "1", "OFFER", -5),
                          ("3aa85f64-5717-4562-b3fc-2c963f66a111", None, "1", "CATEGORY", -5),
                          ("3aa85f64-5717-4562-b3fc-3f66a111", None, "1", "Cfewff", None),
                          ("3aa85f64-5717-4562-b3fc-2c963f66a111", "dqwdqwdwqdqwdwqd", "1", "OFFER", -5),
                          ("3aa85f64-5717-4562-b3fc-2c963f66a111", "3aa85f64-5717-4562-b3fc-2c963f66a111", "1", "OFFER",
                           5)])
def test_import(unit_id, parent_id, name, unit_type, price):
    unit_1 = make_shop_import_unit(unit_id, name, parent_id, price, unit_type)
    update_date = "2022-05-28T21:12:01.000Z"
    with pytest.raises(ValidationError):
        manager.import_nodes([unit_1], update_date)


# не проходит  null надо вместо None печатать
# пока оставлю тк я не уверен так ли нужно выводить
def test_get_str_from_manager():
    unit_1 = make_shop_import_unit("3fa85f64-5717-4562-b3fc-2c963f66a111", "Категория", None, None, "CATEGORY")
    unit_2 = make_shop_import_unit("3fa85f64-5717-4562-b3fc-2c963f66a222", "Оффер 1",
                                   "3fa85f64-5717-4562-b3fc-2c963f66a111", 4, "OFFER")
    unit_3 = make_shop_import_unit("3fa85f64-5717-4562-b3fc-2c963f66a333", "Подкатегория",
                                   "3fa85f64-5717-4562-b3fc-2c963f66a111", None, "CATEGORY")
    unit_4 = make_shop_import_unit("3fa85f64-5717-4562-b3fc-2c963f66a444", "Оффер 2",
                                   "3fa85f64-5717-4562-b3fc-2c963f66a333", 8, "OFFER")
    update_date = "2022-05-26T21:12:01.000Z"
    manager.import_nodes([unit_1, unit_2, unit_3, unit_4], update_date)
    item_str = manager.get_node(unit_1.id)
    assert item_str == expected_str
