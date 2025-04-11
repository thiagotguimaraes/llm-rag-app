from time import sleep
from app.worker import celery_app

@celery_app.task
def add(x: int, y: int) -> int:
    sleep(1)  # simulate workload
    return x + y