import json
import urllib.error
import urllib.parse
import urllib.request

API_BASEURL = "http://localhost:8000"
IMPORT_BATCHES = [
    {
        "items": [
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a777",
                "name": "7",
                "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a666",
                "price": None,
                "type": "CATEGORY"
            },
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a666",
                "name": "6",
                "parentId": None,
                "price": None,
                "type": "CATEGORY"
            },
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a888",
                "name": "8",
                "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a666",
                "price": None,
                "type": "CATEGORY"
            },
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a999",
                "name": "9",
                "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a777",
                "price": None,
                "type": "CATEGORY"
            }
        ],
        "updateDate": "2022-02-03T15:00:00.000Z"
    },
    {
        "items": [
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a444",
                "name": "4",
                "parentId": None,
                "price": None,
                "type": "CATEGORY"
            },
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a222",
                "name": "2",
                "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a111",
                "price": None,
                "type": "CATEGORY"
            },
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a333",
                "name": "3",
                "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a111",
                "price": None,
                "type": "CATEGORY"
            },
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a111",
                "name": "1",
                "parentId": None,
                "price": None,
                "type": "CATEGORY"
            },
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a777",
                "name": "7",
                "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a666",
                "price": None,
                "type": "CATEGORY"
            },
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a666",
                "name": "6",
                "parentId": None,
                "price": None,
                "type": "CATEGORY"
            },
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a888",
                "name": "8",
                "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a666",
                "price": None,
                "type": "CATEGORY"
            },
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a999",
                "name": "9",
                "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a777",
                "price": None,
                "type": "CATEGORY"
            }
        ],
        "updateDate": "2022-02-03T15:00:00.000Z"
    }

]


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
    for index, batch in enumerate(IMPORT_BATCHES):
        print(f"Importing batch {index}")
        status, _ = request("/imports", method="POST", data=batch)

        assert status == 200, f"Expected HTTP status code 200, got {status}"

    print("Test import passed.")
