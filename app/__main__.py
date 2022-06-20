import uvicorn

if __name__ == "__main__":
    uvicorn.run("init_star_app:star_app", host="127.0.0.1", port=8000, reload=True)
