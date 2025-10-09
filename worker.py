from app.celery_utils import celery_app
# import app.tasks


if __name__ == "__main__":
    argv = ["worker", "--loglevel=INFO", "--pool=solo"]
    celery_app.worker_main(argv=argv)
