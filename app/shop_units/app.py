import json
from uuid import UUID
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from app.dto import ShopUnitRequest, Error, DateRequest
from app.shop_units.manager import Manager
from app.exceptions import ValidationError, NotFoundError
from http import HTTPStatus


class Application:
    """
    Application is a top-tree class for application
    """

    def __init__(self, manager: Manager):
        # print("APP")
        self._manager = manager

    async def import_items(self, request: Request):
        """
        Save or update shop units, provided from request body.
        """
        try:
            import_request_json = await request.json()
            import_request = ShopUnitRequest.validate(import_request_json)
            self._manager.import_items(import_request.items, import_request.update_date)
            return Response()
        except (ValidationError, ValueError) as e:
            error = Error()
            error.code = HTTPStatus.BAD_REQUEST
            error.message = "Validation Failed"
            return JSONResponse(dict(error), status_code=HTTPStatus.BAD_REQUEST)

    async def delete_item(self, request: Request):
        """
        Removes item and its children recursively.
        """
        try:
            item_id = UUID(request.path_params['item_id'])
            self._manager.delete_item(item_id)
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

    async def get_item(self, request: Request):
        """
        Get item and provide its children recursively.
        """
        try:
            item_id = UUID(request.path_params['item_id'])
            item = self._manager.get_item(item_id)
            return JSONResponse(item, status_code=200)
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

    async def sales(self, request: Request):
        try:
            date = request.query_params['date']
            date = {"date": date}
            date_request = DateRequest.validate(date)
            items = self._manager.get_sales(date_request.date)
            return JSONResponse(items, status_code=200)
        except ValidationError:
            error = Error()
            error.code = HTTPStatus.BAD_REQUEST
            error.message = "Validation Failed"
            return JSONResponse(dict(error), status_code=HTTPStatus.BAD_REQUEST)
