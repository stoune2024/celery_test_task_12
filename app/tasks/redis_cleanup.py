from app.celery_utils import celery_app
from redis import Redis


@celery_app.task
def daily_report_cleanup():
    r = Redis(
        host="redis",  # Для Docker Compose
        port=6379,
        db=0,
        # password="redis",
        decode_responses=True,
        # username="default",
    )
    for key in r.scan_iter("celery-task-meta-*"):
        print(key)
        r.delete(key)
    return "Cleanup succeeded!"
