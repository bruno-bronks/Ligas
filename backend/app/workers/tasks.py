"""
Football Intelligence Dashboard - Celery Tasks
Background task definitions for data sync, predictions, and notifications.
"""

import asyncio
from loguru import logger

from app.workers import celery_app
from app.core.database import async_session_factory


def run_async(coro):
    """Helper to run async functions in Celery sync context."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery_app.task(name="app.workers.tasks.sync_all_leagues_task")
def sync_all_leagues_task(season: int = 2024):
    """Sync all leagues from API-Football."""
    async def _sync():
        async with async_session_factory() as session:
            from app.services.sync_service import SyncService
            service = SyncService(session)
            result = await service.sync_all(season_year=season)
            await session.commit()
            logger.info(f"Full sync completed: {result}")
            return result

    return run_async(_sync())


@celery_app.task(name="app.workers.tasks.sync_fixtures_task")
def sync_fixtures_task(season: int = 2024):
    """Sync fixtures for all leagues."""
    async def _sync():
        async with async_session_factory() as session:
            from app.services.sync_service import SyncService
            from app.core.config import LEAGUES_CONFIG

            service = SyncService(session)
            results = {}
            for league in LEAGUES_CONFIG:
                result = await service.sync_fixtures(league["code"], season)
                results[league["code"]] = result
            await session.commit()
            logger.info(f"Fixtures sync completed: {results}")
            return results

    return run_async(_sync())


@celery_app.task(name="app.workers.tasks.compute_predictions_task")
def compute_predictions_task():
    """Compute predictions for upcoming matches."""
    async def _predict():
        async with async_session_factory() as session:
            from app.services.prediction_service import PredictionService
            from app.repositories.match_repository import MatchRepository
            from sqlalchemy import select
            from app.models.season import Season
            from app.models.match import Match

            pred_service = PredictionService(session)
            match_repo = MatchRepository(session)

            # Get all current seasons
            seasons = (await session.execute(
                select(Season).where(Season.is_current == True)
            )).scalars().all()

            count = 0
            for season in seasons:
                upcoming = await match_repo.get_upcoming(season.id)
                for match in upcoming:
                    if not match.prediction:
                        prediction = await pred_service.predict_match(match)
                        session.add(prediction)
                        count += 1

            await session.commit()
            logger.info(f"Predictions computed for {count} matches")
            return {"predictions_created": count}

    return run_async(_predict())


@celery_app.task(name="app.workers.tasks.send_weekly_digest_task")
def send_weekly_digest_task():
    """Send weekly G3 vs Z3 digest via WhatsApp and Telegram."""
    async def _send():
        async with async_session_factory() as session:
            from app.services.notification_service import NotificationService
            from app.repositories.match_repository import MatchRepository

            match_repo = MatchRepository(session)
            g3z3_matches = await match_repo.get_g3_vs_z3()

            upcoming = [m for m in g3z3_matches if m.status == "NS"]

            match_data = [
                {
                    "home_team": m.home_team.name if m.home_team else "?",
                    "away_team": m.away_team.name if m.away_team else "?",
                    "match_date": m.match_date.strftime("%d/%m %H:%M"),
                    "league_name": m.season.league.name if m.season and m.season.league else "?",
                    "status": m.status,
                }
                for m in upcoming[:15]
            ]

            notif_service = NotificationService(session)
            result = await notif_service.send_g3_vs_z3_digest(match_data)
            await session.commit()
            logger.info(f"Weekly digest sent: {result}")
            return result

    return run_async(_send())
