"""
Admin API endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_admin_user
from app.services.sync_service import SyncService

router = APIRouter()


@router.post("/sync")
async def trigger_sync(
    season: int = 2024,
    db: AsyncSession = Depends(get_db),
):
    """Trigger a full data sync from API-Football."""
    sync_service = SyncService(db)
    results = await sync_service.sync_all(season_year=season)
    return {"status": "completed", "results": results}


@router.post("/sync/{league_code}")
async def sync_league(
    league_code: str,
    season: int = 2024,
    db: AsyncSession = Depends(get_db),
):
    """Sync a specific league."""
    sync_service = SyncService(db)

    teams = await sync_service.sync_teams(league_code.upper(), season)
    standings = await sync_service.sync_standings(league_code.upper(), season)
    fixtures = await sync_service.sync_fixtures(league_code.upper(), season)

    return {
        "league": league_code.upper(),
        "teams": teams,
        "standings": standings,
        "fixtures": fixtures,
    }


@router.post("/seed-leagues")
async def seed_leagues(db: AsyncSession = Depends(get_db)):
    """Seed the 14 leagues from config."""
    sync_service = SyncService(db)
    result = await sync_service.sync_leagues()
    return {"status": "completed", "result": result}


@router.post("/compute-predictions")
async def compute_predictions(db: AsyncSession = Depends(get_db)):
    """Trigger predictions calculation for upcoming matches."""
    from app.services.prediction_service import PredictionService
    from app.repositories.match_repository import MatchRepository
    from app.models.season import Season
    from sqlalchemy import select

    pred_service = PredictionService(db)
    match_repo = MatchRepository(db)

    # Get all current seasons
    seasons = (await db.execute(
        select(Season).where(Season.is_current == True)
    )).scalars().all()

    count = 0
    for season in seasons:
        upcoming = await match_repo.get_upcoming(season.id)
        for match in upcoming:
            if not match.prediction:
                prediction = await pred_service.predict_match(match)
                db.add(prediction)
                count += 1

    await db.commit()
    return {"status": "completed", "predictions_created": count}


@router.post("/send-digest")
async def send_digest(db: AsyncSession = Depends(get_db)):
    """Send weekly G3 vs Z3 digest via WhatsApp and Telegram."""
    from app.services.notification_service import NotificationService
    from app.repositories.match_repository import MatchRepository

    match_repo = MatchRepository(db)
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

    notif_service = NotificationService(db)
    result = await notif_service.send_g3_vs_z3_digest(match_data)
    await db.commit()
    return {"status": "completed", "result": result}

