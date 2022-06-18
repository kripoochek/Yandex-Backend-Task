from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Union
from dto import ShopUnitRequest, Error
from shop_units.manager_interface import ManagerInterface
from shop_units.manager import Manager
from exceptions import ValidationError, NotFoundError
from shop_units.postgres_dao import PostgresDAO

router = FastAPI()
dao = PostgresDAO()
manager = Manager(dao)


@router.post("/imports")
async def imports(shop_unit_request: ShopUnitRequest, response: Response):
    try:
        shop_unit_request = dict(shop_unit_request)
        manager.import_nodes(shop_unit_request["items"], shop_unit_request["updateDate"])
        response.status_code = 200
    except ValidationError:
        error = Error()
        error.code = 400
        error.message = "Validation Failed"
        response.status_code = 400
        return error
    return response


@router.delete("/delete/{item_id}")
async def delete_item(item_id: str, response: Response):
    try:
        manager.delete_node(item_id)
    except ValidationError:
        error = Error()
        error.code = 400
        error.message = "Validation Failed"
        response.status_code = 400
        return error
    except NotFoundError:
        error = Error()
        error.code = 404
        error.message = "Item not found"
        response.status_code = 404
        return error
    return response


@router.get("/nodes/{item_id}")
async def imports(item_id: str, response: Response):
    try:
        manager.get_node(item_id)
    except ValidationError:
        error = Error()
        error.code = 400
        error.message = "Validation Failed"
        response.status_code = 400
        return error
    except NotFoundError:
        error = Error()
        error.code = 404
        error.message = "Item not found"
        response.status_code = 404
        return error
    return response
