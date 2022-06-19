import json

from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.routing import Route
from starlette.schemas import SchemaGenerator
from dto import ShopUnitRequest, Error, ShopUnitImport, ShopUnit
from shop_units.manager import Manager
from exceptions import ValidationError, NotFoundError
from shop_units.postgres_dao import PostgresDAO
from http import HTTPStatus

dao: PostgresDAO
manager: Manager
schemas: SchemaGenerator


def make_serializable(unit: ShopUnit) -> dict:
    unit = dict(unit)
    if "children" in unit:
        if unit["children"] is not None:
            for i in range(len(unit["children"])):
                unit["children"][i] = make_serializable(unit["children"][i])
    return unit


def request_json_to_shop_unit_request(request_js: dict) -> ShopUnitRequest:
    if ("items" not in request_js) or ("updateDate" not in request_js):
        raise ValidationError
    items = list()
    for item in request_js["items"]:
        items.append(ShopUnitImport(**item))
    return ShopUnitRequest(items=items, updateDate=request_js["updateDate"])


def startup():
    global dao
    global manager
    global schemas
    dao = PostgresDAO()
    manager = Manager(dao)
    schemas = SchemaGenerator(
        {"openapi": "3.0.0", "info": {"title": "Example API", "version": "1.0"}}
    )


async def imports(request: Request):
    try:
        response = Response()
        shop_unit_request_json = await request.json()
        shop_unit_request = request_json_to_shop_unit_request(shop_unit_request_json)
        manager.import_nodes(shop_unit_request.items, shop_unit_request.updateDate)
        return response
    except ValidationError:
        error = Error()
        error.code = HTTPStatus.BAD_REQUEST
        error.message = "Validation Failed"
        response.body = dict(error)
        return JSONResponse(response.body, status_code=HTTPStatus.BAD_REQUEST)


def delete_item(request: Request):
    try:
        response = Response()
        item_id = request.path_params['item_id']
        manager.delete_node(item_id)
        return response
    except ValidationError:
        error = Error()
        error.code = HTTPStatus.BAD_REQUEST
        error.message = "Validation Failed"
        response.body = dict(error)
        response.status_code = HTTPStatus.BAD_REQUEST
        return response
    except NotFoundError:
        error = Error()
        error.code = HTTPStatus.NOT_FOUND
        error.message = "Item not found"
        response.body = dict(error)
        response.status_code = HTTPStatus.NOT_FOUND
        return response


def get_item(request: Request):
    try:
        response = Response()
        item_id = request.path_params['item_id']
        item = manager.get_node(item_id)
        response.body = make_serializable(item)
        return JSONResponse(response.body, status_code=200)
    except ValidationError:
        error = Error()
        error.code = HTTPStatus.BAD_REQUEST
        error.message = "Validation Failed"
        response.body = dict(error)
        return JSONResponse(response.body, status_code=HTTPStatus.BAD_REQUEST)
    except NotFoundError:
        error = Error()
        error.code = HTTPStatus.NOT_FOUND
        error.message = "Item not found"
        response.body = dict(error)
        return JSONResponse(response.body, status_code=HTTPStatus.NOT_FOUND)


def openapi_schema(request):
    return schemas.OpenAPIResponse(request=request)


routes = [
    Route('/imports', imports, methods=["POST"]),
    Route('/delete/{item_id}', delete_item, methods=["DELETE"]),
    Route('/nodes/{item_id}', get_item, methods=["GET"]),
    Route('/schema', endpoint=openapi_schema, include_in_schema=False)
]
