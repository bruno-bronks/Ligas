"""
Football Intelligence Dashboard - Celery Worker Configuration
Background tasks and periodic scheduling.
"""

from celery import Celery
from celery.schedules import crontab

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "football_intelligence",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="America/Sao_Paulo",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

# Periodic tasks schedule
celery_app.conf.beat_schedule = {
    "sync-all-leagues": {
        "task": "app.workers.tasks.sync_all_leagues_task",
        "schedule": crontab(minute=0, hour="*/6"),  # Every 6 hours
    },
    "sync-fixtures": {
        "task": "app.workers.tasks.sync_fixtures_task",
        "schedule": crontab(minute=0, hour="*/2"),  # Every 2 hours
    },
    "compute-predictions": {
        "task": "app.workers.tasks.compute_predictions_task",
        "schedule": crontab(minute=0, hour=6),  # Daily at 06:00
    },
    "send-weekly-g3z3-digest": {
        "task": "app.workers.tasks.send_weekly_digest_task",
        "schedule": crontab(minute=0, hour=8, day_of_week=1),  # Monday 08:00
    },
}
