from starlette.applications import Starlette
from handler import routes, startup
import uvicorn


app = Starlette(debug=True, routes=routes, on_startup=[startup])
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
