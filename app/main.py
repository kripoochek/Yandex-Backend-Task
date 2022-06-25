import uvicorn


if __name__ == "__main__":
    uvicorn.run("app.init_star_app:star_app", host="0.0.0.0", port=80)
