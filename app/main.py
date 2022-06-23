import uvicorn
from starlette.applications import Starlette

from app.init_star_app import routes

star_app = Starlette(debug=True, routes=routes)


