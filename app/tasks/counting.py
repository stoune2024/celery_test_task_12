# файл, созданный нами в прошлом уроке
from app.celery_utils import celery_app


@celery_app.task
def count_numbers(n: int) -> int:
    """Считает сумму чисел от 1 до n."""
    return sum(range(1, n + 1))
