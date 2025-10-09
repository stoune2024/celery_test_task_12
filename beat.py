from app.celery_utils import celery_app


if __name__ == "__main__":
    argv = ["beat", "--loglevel=INFO"]
    celery_app.start(argv=argv)  # Запуск планировщика
