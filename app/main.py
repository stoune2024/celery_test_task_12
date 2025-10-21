from fastapi import FastAPI
from uvicorn import run
from app.tasks.counting import count_numbers
from app.celery_utils import celery_app
from app.tasks.unreliable import unreliable_task
from app.tasks.send_email import send_email
from pydantic import BaseModel, EmailStr
from app.settings import SettingsDep


app = FastAPI()


class EmailBody(BaseModel):
    subject: str
    to_who: EmailStr
    body_content: str


@app.get("/")
def home():
    return {"message": "FastAPI работает вместе с Celery!"}


@app.post("/count/{n}")
def run_count_task(n: int):
    """Запускаем задачу подсчёта чисел."""
    task = count_numbers.delay(n)  # отправляем в Celery
    return {"task_id": task.id, "status": "Задача поставлена в очередь"}


@app.post("/unreliable/{n}")
def run_unreliable_task(n: int):
    task = unreliable_task.delay(n)
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


@app.post("/send-email")
def send_email_func(body: EmailBody, settings: SettingsDep):
    """
    Запускам задачу отправки электронного письма
    """
    task = send_email.delay(
        body.subject,
        settings.SMTP_LOGIN,
        body.to_who,
        body.body_content,
        settings.SMTP_HOST,
        settings.SMTP_PASSWORD_FOR_APP,
    )
    return {"message": "Письмо успешно отправлено", "task_id": task.id}


if __name__ == "__main__":
    run(
        app="main:app",
        reload=True,
        log_level="debug",
        host="localhost",
        port=8000,
    )
