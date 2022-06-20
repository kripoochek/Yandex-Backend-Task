import json
from uuid import UUID
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from app.dto import ShopUnitRequest, Error
from app.shop_units.manager import Manager
from app.exceptions import ValidationError, NotFoundError
from http import HTTPStatus


def homepage(request):
    return JSONResponse(dict('Hello, world!'))


class Application:
    """
    Application is a top-tree class for application
    """

    def __init__(self, manager: Manager):
        # print("APP")
        self._manager = manager

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
