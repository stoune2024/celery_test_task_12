from app.celery_utils import celery_app


if __name__ == "__main__":
    argv = ["worker", "--loglevel=INFO"]  # --pool=solo - Для Windows
    celery_app.worker_main(argv=argv)  # Запуск рабочего узла
