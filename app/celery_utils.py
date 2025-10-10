from celery.schedules import crontab, Celery


def make_celery():
    celery = Celery(
        "worker",
        broker="redis://default:redis@localhost:6379/3",  # очередь задач
        backend="redis://default:redis@localhost:6379/3",  # хранение результатов
    )

    celery.conf.update(
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        timezone="UTC",
        enable_utc=True,
        beat_schedule={
            "daily-report-cleanup-task": {
                "task": "app.tasks.redis_cleanup.daily_report_cleanup",
                "schedule": crontab(minute="*/5"),  # Каждые 5 минут
            },
            "daily-report-task": {
                "task": "app.tasks.periodic.daily_report",
                # "schedule": crontab(hour=9, minute=0),  # Каждый понедельник в 8 утра
                "schedule": crontab(minute="*/1"),  # Каждую минуту
            },
        },
    )

    return celery


celery_app = make_celery()


celery_app.config_from_object("app.celery_utils.celery_app")
celery_app.autodiscover_tasks(["app.tasks"])  # файл с celery задачами
