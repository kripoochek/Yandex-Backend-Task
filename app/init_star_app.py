from dotenv import load_dotenv
import os
from typing import List
import psycopg2
from starlette.applications import Starlette
from starlette.routing import Route
from yoyo.migrations import Migration

from app.shop_units.app import Application
from app.shop_units.manager import Manager
from app.shop_units.dao import PostgresDAO, DAO
from yoyo import read_migrations

load_dotenv()
routes = []
star_app: Starlette


def bind_routes(app: Application) -> List[Route]:
    global routes
    routes = [
        Route('/imports', app.import_items, methods=["POST"]),
        Route('/delete/{item_id}', app.delete_item, methods=["DELETE"]),
        Route('/nodes/{item_id}', app.get_item, methods=["GET"]),
        Route('/sales', app.sales, methods=["GET"]),
        Route('/node/{item_id}/statistic', app.get_statistic, methods=["GET"])
    ]
    return routes


def migration_up(connection):
    migrations = read_migrations('../db/migrations/')
    with connection.cursor() as cursor:
        for migration in migrations.items:
            source = migration.source
            cursor.execute(source)


def initialize():
    conn = psycopg2.connect(dsn=os.environ["PG_ADDRESS"])
    migration_up(conn)
    dao: DAO = PostgresDAO(conn, 'shop_units')
    manager = Manager(dao)
    app = Application(manager)
    bind_routes(app)


initialize()
