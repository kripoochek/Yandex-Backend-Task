import json
from uuid import UUID
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from dto import ShopUnitRequest, Error
from shop_units.manager import Manager
from exceptions import ValidationError, NotFoundError
from http import HTTPStatus

"""
def make_serializable(unit: ShopUnit) -> dict:
    unit = dict(unit)
    unit["id"] = str(unit["id"])
    if unit["parent_id"] is not None:
        unit["parent_id"] = str(unit["parent_id"])
    unit["date"] = unit["date"].strftime("%Y-%m-%dT%H:%M:%S.000Z")
    if "children" in unit:
        if unit["children"] is not None:
            for i in range(len(unit["children"])):
                unit["children"][i] = make_serializable(unit["children"][i])
    return unit


def request_json_to_shop_unit_request(request_js: dict) -> ShopUnitRequest:
    if ("items" not in request_js) or ("updateDate" not in request_js) or (len(request_js) != 2):
        raise ValidationError
    items = list()
    try:
        for item in request_js["items"]:
            items.append(ShopUnitImport.validate(item))
        shop_unit_request = ShopUnitRequest.validate({"items": items, "updateDate": request_js["updateDate"]})
    except ValueError:
        raise ValidationError
    return shop_unit_request
"""


class Application:
    """
    Application is a top-tree class for application
    """

    def __init__(self, manager: Manager):
        self._manager = manager

    def homepage(self, request):
        return JSONResponse(dict('Hello, world!'))

    async def import_nodes(self, request: Request):
        """
        Save or update shop units, provided from request body.
        """
        try:
            import_request_json = await request.json()
            import_request = ShopUnitRequest.validate(import_request_json)
            self._manager.import_nodes(import_request.items, import_request.update_date)
            return Response()
        except (ValidationError, ValueError) as e:
            error = Error()
            error.code = HTTPStatus.BAD_REQUEST
            error.message = "Validation Failed"
            return JSONResponse(dict(error), status_code=HTTPStatus.BAD_REQUEST)

    async def delete_node(self, request: Request):
        """
        Removes node and its children recursively.
        """
        try:
            node_id = UUID(request.path_params['item_id'])
            self._manager.delete_node(node_id)
            return Response()
        except (ValidationError, ValueError) as e:
            error = Error()
            error.code = HTTPStatus.BAD_REQUEST
            error.message = "Validation Failed"
            return JSONResponse(dict(error), status_code=HTTPStatus.BAD_REQUEST)
        except NotFoundError:
            error = Error()
            error.code = HTTPStatus.NOT_FOUND
            error.message = "Item not found"
            return JSONResponse(dict(error), status_code=HTTPStatus.NOT_FOUND)

    async def get_node(self, request: Request):
        """
        Get node and provide its children recursively.
        """
        try:
            node_id = UUID(request.path_params['item_id'])
            node = self._manager.get_node(node_id)
            return JSONResponse(json.loads(node.json()), status_code=200)
        except (ValidationError, ValueError) as e:
            error = Error()
            error.code = HTTPStatus.BAD_REQUEST
            error.message = "Validation Failed"
            return JSONResponse(dict(error), status_code=HTTPStatus.BAD_REQUEST)
        except NotFoundError:
            error = Error()
            error.code = HTTPStatus.NOT_FOUND
            error.message = "Item not found"
            return JSONResponse(dict(error), status_code=HTTPStatus.NOT_FOUND)
