from fastapi import FastAPI
from uvicorn import run

app = FastAPI()


@app.get("/")
def home():
    return {"message": "FastAPI работает вместе с Celery!"}


if __name__ == "__main__":
    run(
        app="main:app",
        reload=True,
        log_level="debug",
        host="localhost",
        port=8000,
    )
