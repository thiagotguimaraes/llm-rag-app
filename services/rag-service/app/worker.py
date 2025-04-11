from celery import Celery

celery_app = Celery(
    "rag_service_tasks",
    broker="redis://redis:6379/0",  # for Docker
    backend="redis://redis:6379/0",
)

celery_app.autodiscover_tasks(["app.tasks.add"])

celery_app.conf.task_routes = {"app.tasks.add.add": {"queue": "default"}}
