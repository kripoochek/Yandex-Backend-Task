from dotenv import load_dotenv
import os
from typing import List
import psycopg2
from starlette.applications import Starlette
from starlette.routing import Route
import uvicorn
from shop_units.app import Application
from shop_units.manager import Manager
from shop_units.dao import PostgresDAO, DAO

load_dotenv()
routes = []


def bind_routes(app: Application) -> List[Route]:
    global routes
    routes = [
        Route('/', app.homepage, methods=["GET"]),
        Route('/imports', app.import_nodes, methods=["POST"]),
        Route('/delete/{item_id}', app.delete_node, methods=["DELETE"]),
        Route('/nodes/{item_id}', app.get_node, methods=["GET"]),
    ]
    return routes


def startup():
    conn = psycopg2.connect(
        host=os.environ["host"],
        user=os.environ["username"],
        password=os.environ["password"],
        database=os.environ["db_name"]
    )
    dao: DAO = PostgresDAO(conn, os.environ["db_name"])
    manager = Manager(dao)
    app = Application(manager)
    bind_routes(app)


star_app = Starlette(debug=True, routes=routes, on_startup=[startup])

if __name__ == "__main__":
    uvicorn.run("__main__:star_app", host="127.0.0.1", port=8000, reload=True)
