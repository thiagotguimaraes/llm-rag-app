from celery import Celery
from dotenv import load_dotenv
import os
load_dotenv()

REDIS_PORT = os.getenv("REDIS_PORT")

celery_app = Celery(
    "rag_service_tasks",
    broker=f"redis://redis:{REDIS_PORT}/0",  # for Docker
    backend=f"redis://redis:{REDIS_PORT}/0",
)

celery_app.autodiscover_tasks(["app.tasks.add", "app.tasks.embed", "app.tasks.embedding"], force=True)

celery_app.conf.task_default_queue = "default"
