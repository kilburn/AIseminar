from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "tweeteval_worker",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.workers.tasks"]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=settings.processing_timeout,
    task_soft_time_limit=settings.processing_timeout - 60,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    result_expires=3600,  # 1 hour
    beat_schedule={
        # Example scheduled tasks
        "cleanup-expired-exports": {
            "task": "app.workers.tasks.cleanup_expired_exports",
            "schedule": crontab(hour=2, minute=0),  # Run daily at 2 AM
        },
        "update-system-metrics": {
            "task": "app.workers.tasks.update_system_metrics",
            "schedule": crontab(minute="*/15"),  # Run every 15 minutes
        },
    },
)

# Optional: Configure task routing for different task types
celery_app.conf.task_routes = {
    "app.workers.tasks.process_dataset": {"queue": "processing"},
    "app.workers.tasks.analyze_tweets": {"queue": "nlp"},
    "app.workers.tasks.generate_embeddings": {"queue": "embeddings"},
    "app.workers.tasks.export_data": {"queue": "export"},
}