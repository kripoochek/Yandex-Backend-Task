import uvicorn
from starlette.applications import Starlette
from app.init_star_app import routes

star_app = Starlette(debug=True, routes=routes)
if __name__ == "__main__":
    uvicorn.run("main:star_app", host="0.0.0.0", port=80)
