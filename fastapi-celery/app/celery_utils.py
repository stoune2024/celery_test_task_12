from celery import Celery


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
    )

    return celery


celery_app = make_celery()
