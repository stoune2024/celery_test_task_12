from app.celery_utils import celery_app


@celery_app.task(bind=True, max_retries=3)
def unreliable_task(self, n: int):
    """
    Задача может случайно падать.
    Если n чётное — генерируем ошибку для демонстрации retries.
    """
    try:
        if n % 2 == 0:
            raise ValueError("Случайная ошибка! Попробуем снова...")
        return n * 2
    except Exception as exc:
        # Повторная попытка через 5 секунд
        raise self.retry(exc=exc, countdown=5)
