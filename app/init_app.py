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


def bind_routes(application: Application) -> List[Route]:
    global routes
    routes = [
        Route('/imports', application.import_items, methods=["POST"]),
        Route('/delete/{item_id}', application.delete_item, methods=["DELETE"]),
        Route('/nodes/{item_id}', application.get_item, methods=["GET"]),
        Route('/sales', application.sales, methods=["GET"]),
        Route('/node/{item_id}/statistic', application.get_statistic, methods=["GET"])
    ]
    return routes


def initialize():
    conn = psycopg2.connect(dsn=os.environ["PG_ADDRESS"])
    dao: DAO = PostgresDAO(conn)
    manager = Manager(dao)
    application = Application(manager)
    bind_routes(application)


initialize()
app = Starlette(debug=True, routes=routes)
