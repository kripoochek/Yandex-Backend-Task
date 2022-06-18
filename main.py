from exceptions import ValidationError
from handler import router
from fastapi import FastAPI
import uvicorn


def get_application(include_router):
    return include_router


app = get_application(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
