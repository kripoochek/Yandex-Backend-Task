import json
from uuid import UUID
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from app.dto import ShopUnitRequest, Error, DateRequest
from app.shop_units.manager import Manager
from app.exceptions import ValidationError, NotFoundError
from http import HTTPStatus


def make_error(code: int, message: str) -> JSONResponse:
    error = Error()
    error.code = code
    error.message = message
    return JSONResponse(dict(error), status_code=code)


class Application:
    """
    Application is a top-tree class for application
    """

    def __init__(self, manager: Manager):
        self._manager = manager

    async def import_items(self, request: Request):
        """
        Save or update shop units, provided from request body.
        """
        try:
            import_request_json = await request.json()
            import_request = ShopUnitRequest.validate(import_request_json)
            date_test = {"date": import_request.update_date}
            DateRequest.validate(date_test)
            self._manager.import_items(import_request.items, import_request.update_date)
            return Response()
        except (ValidationError, ValueError):
            return make_error(HTTPStatus.BAD_REQUEST, "Validation Failed")

    async def delete_item(self, request: Request):
        """
        Removes item and its children recursively.
        """
        try:
            item_id = UUID(request.path_params['item_id'])
            self._manager.delete_item(item_id)
            return Response()
        except (ValidationError, ValueError):
            return make_error(HTTPStatus.BAD_REQUEST, "Validation Failed")
        except NotFoundError:
            return make_error(HTTPStatus.NOT_FOUND, "Item not found")

    async def get_item(self, request: Request):
        """
        Get item and provide its children recursively.
        """
        try:
            item_id = UUID(request.path_params['item_id'])
            item = self._manager.get_item(item_id)
            return JSONResponse(json.loads(item.json()), status_code=200)
        except (ValidationError, ValueError):
            return make_error(HTTPStatus.BAD_REQUEST, "Validation Failed")
        except NotFoundError:
            return make_error(HTTPStatus.NOT_FOUND, "Item not found")

    async def sales(self, request: Request):
        """
        Getting a list of products
        whose price has been updated in the last 24 hours from the time passed in the request.
        """
        try:
            date = request.query_params['date']
            date = {"date": date}
            date = DateRequest.validate(date).date
            items = self._manager.get_sales(date)
            return JSONResponse(items, status_code=200)
        except ValidationError:
            return make_error(HTTPStatus.BAD_REQUEST, "Validation Failed")

    async def get_statistic(self, request: Request):
        """
        Obtaining statistics (history of updates) on the price of a product(provided from path params)
        for a given interval provided from query_params.
        """
        try:
            item_id = UUID(request.path_params['item_id'])
            date_start = request.query_params['dateStart']
            date_start = {"date": date_start}
            date_start = DateRequest.validate(date_start).date
            date_end = request.query_params['dateEnd']
            date_end = {"date": date_end}
            date_end = DateRequest.validate(date_end).date
            items = self._manager.statistic(item_id, date_start, date_end)
            return JSONResponse(items, status_code=200)
        except (ValidationError, ValueError):
            return make_error(HTTPStatus.BAD_REQUEST, "Validation Failed")
        except NotFoundError:
            return make_error(HTTPStatus.NOT_FOUND, "Item not found")
