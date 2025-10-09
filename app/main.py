from fastapi import FastAPI
from uvicorn import run
from app.tasks.counting import count_numbers
from app.celery_utils import celery_app

app = FastAPI()


@app.get("/")
def home():
    return {"message": "FastAPI работает вместе с Celery!"}


@app.post("/count/{n}")
def run_count_task(n: int):
    """Запускаем задачу подсчёта чисел."""
    task = count_numbers.delay(n)  # отправляем в Celery
    return {"task_id": task.id, "status": "Задача поставлена в очередь"}


@app.get("/status/{task_id}")
def get_task_status(task_id: str):
    """Проверяем статус задачи."""
    task_result = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result,
    }


if __name__ == "__main__":
    run(
        app="main:app",
        reload=True,
        log_level="debug",
        host="localhost",
        port=8000,
    )
