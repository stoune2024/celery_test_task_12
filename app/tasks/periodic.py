from app.celery_utils import celery_app
from datetime import datetime


@celery_app.task
def daily_report():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Генерация ежедневного отчета: {now}")
    return f"Report is generated on {now}"
