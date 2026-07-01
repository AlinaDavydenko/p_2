from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "bot_service",
    broker=settings.RABBITMQ_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)

# Explicit import (in addition to autodiscover) so the "llm_request" task
# is always registered, even if autodiscovery is skipped in some entrypoints.
celery_app.autodiscover_tasks(["app.tasks"])
import app.tasks.llm_tasks  # noqa: E402,F401
