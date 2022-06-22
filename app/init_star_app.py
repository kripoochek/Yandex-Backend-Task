from dotenv import load_dotenv
import os
from typing import List
import psycopg2
from starlette.applications import Starlette
from starlette.routing import Route
from app.shop_units.app import Application
from app.shop_units.manager import Manager
from app.shop_units.dao import PostgresDAO, DAO

load_dotenv()
routes = []
star_app: Starlette


def bind_routes(app: Application) -> List[Route]:
    global routes
    routes = [
        Route('/imports', app.import_items, methods=["POST"]),
        Route('/delete/{item_id}', app.delete_item, methods=["DELETE"]),
        Route('/nodes/{item_id}', app.get_item, methods=["GET"]),
        Route('/sales', app.sales, methods=["GET"])
    ]
    return routes


def startup():
    pass


def initialize():
    conn = psycopg2.connect(
        host=os.environ["host"],
        user=os.environ["username"],
        password=os.environ["password"],
        database=os.environ["db_name"]
    )
    dao: DAO = PostgresDAO(conn, 'shop_units')
    manager = Manager(dao)
    app = Application(manager)
    bind_routes(app)


initialize()
star_app = Starlette(debug=True, routes=routes, on_startup=[startup])
