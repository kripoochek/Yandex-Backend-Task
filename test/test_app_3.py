import json
import urllib.error
import urllib.parse
import urllib.request

"https://history-1816.usr.yandex-academy.ru"
API_BASEURL = "https://history-1816.usr.yandex-academy.ru"
"""
тестирование обновления
- тип изменить нельзя
- цену нельзя обновить до неправильного значения
- при обновлении подкатегории обновляется дата родителя 
"""
IMPORT_BATCHES_200 = [
    {
        "items": [
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a111",
                "name": "father",
                "parentId": None,
                "price": None,
                "type": "CATEGORY"
            },
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a222",
                "name": "son",
                "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a111",
                "price": 5,
                "type": "OFFER"
            }
        ],
        "updateDate": "2022-02-03T15:00:00.000Z"
    },
    {
        "items": [
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a222",
                "name": "son",
                "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a111",
                "price": 5,
                "type": "OFFER"
            }
        ],
        "updateDate": "2023-02-03T15:00:00.000Z"
    }
]
IMPORT_BATCHES_400 = [
    {
        "items": [
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a111",
                "name": "father",
                "parentId": None,
                "price": None,
                "type": "OFFER"
            }
        ],
        "updateDate": "2022-02-03T15:00:00.000Z"
    },
    {
        "items": [
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a222",
                "name": "son",
                "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a111",
                "price": None,
                "type": "OFFER"
            }
        ],
        "updateDate": "2022-02-03T15:00:00.000Z"
    },
    {
        "items": [
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a222",
                "name": "son",
                "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a111",
                "price": -5,
                "type": "OFFER"
            }
        ],
        "updateDate": "2022-02-03T15:00:00.000Z"
    }
]
DELETE_ID = ["3fa85f64-5717-4562-b3fc-2c963f66a111"]


def request(path, method="GET", data=None, json_response=False):
    try:
        params = {
            "url": f"{API_BASEURL}{path}",
            "method": method,
            "headers": {},
        }

        if data:
            params["data"] = json.dumps(
                data, ensure_ascii=False).encode("utf-8")
            params["headers"]["Content-Length"] = len(params["data"])
            params["headers"]["Content-Type"] = "application/json"

        req = urllib.request.Request(**params)

        with urllib.request.urlopen(req) as res:
            res_data = res.read().decode("utf-8")
            if json_response:
                res_data = json.loads(res_data)
            return (res.getcode(), res_data)
    except urllib.error.HTTPError as e:
        return (e.getcode(), None)


def test_import():
    for index, batch in enumerate(IMPORT_BATCHES_200):
        print(f"Importing batch {index}")
        status, _ = request("/imports", method="POST", data=batch)
        assert status == 200, f"Expected HTTP status code 200, got {status}"
    for index, batch in enumerate(IMPORT_BATCHES_400):
        print(f"Importing batch {index}")
        status, _ = request("/imports", method="POST", data=batch)
        assert status == 400, f"Expected HTTP status code 400, got {status}"

    print("Test import passed.")


def test_delete():
    for index, del_id in enumerate(DELETE_ID):
        status, _ = request(f"/delete/{del_id}", method="DELETE")

        assert status == 200, f"Expected HTTP status code 200, got {status}"
