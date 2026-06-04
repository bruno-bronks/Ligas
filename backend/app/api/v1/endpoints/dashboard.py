"""
Dashboard API endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.league import League
from app.models.match import Match
from app.models.season import Season
from app.models.standing import Standing
from app.models.team import Team
from app.repositories.match_repository import MatchRepository

router = APIRouter()


@router.get("/overview")
async def dashboard_overview(db: AsyncSession = Depends(get_db)):
    """Dashboard aggregate data across all leagues."""
    # Counts
    leagues_count = (await db.execute(select(func.count()).select_from(League))).scalar_one()
    teams_count = (await db.execute(select(func.count()).select_from(Team))).scalar_one()
    matches_count = (await db.execute(select(func.count()).select_from(Match))).scalar_one()

    # Total goals
    goals_result = await db.execute(
        select(
            func.coalesce(func.sum(Match.home_score), 0) +
            func.coalesce(func.sum(Match.away_score), 0)
        ).where(Match.status == "FT")
    )
    total_goals = goals_result.scalar_one() or 0

    # League summaries
    leagues = (await db.execute(
        select(League).where(League.is_active == True).order_by(League.country)
    )).scalars().all()

    league_summaries = []
    for league in leagues:
        # Get current season
        season = (await db.execute(
            select(Season)
            .where(Season.league_id == league.id, Season.is_current == True)
            .order_by(Season.year.desc())
            .limit(1)
        )).scalars().first()

        leader = None
        leader_points = None
        if season:
            top_standing = (await db.execute(
                select(Standing)
                .options()
                .where(Standing.season_id == season.id)
                .order_by(Standing.position)
                .limit(1)
            )).scalar_one_or_none()
            if top_standing:
                team = await db.get(Team, top_standing.team_id)
                leader = team.name if team else None
                leader_points = top_standing.points

        league_summaries.append({
            "code": league.code,
            "name": league.name,
            "country": league.country,
            "flag_emoji": league.flag_emoji,
            "leader_team": leader,
            "leader_points": leader_points,
        })

    # G3 vs Z3 upcoming count
    g3z3_count = (await db.execute(
        select(func.count()).select_from(Match).where(
            Match.is_g3_vs_z3 == True, Match.status == "NS"
        )
    )).scalar_one()

    return {
        "total_leagues": leagues_count,
        "total_teams": teams_count,
        "total_matches": matches_count,
        "total_goals": total_goals,
        "leagues": league_summaries,
        "upcoming_g3_vs_z3": g3z3_count,
    }


@router.get("/highlights")
async def dashboard_highlights(db: AsyncSession = Depends(get_db)):
    """Dashboard highlighted matches (G3 vs Z3, live, recent)."""
    repo = MatchRepository(db)

    live = await repo.get_live_matches()
    g3z3 = await repo.get_g3_vs_z3()

    def serialize(m):
        return {
            "id": m.id,
            "home_team": m.home_team.name if m.home_team else "?",
            "away_team": m.away_team.name if m.away_team else "?",
            "home_team_logo": m.home_team.logo_url if m.home_team else None,
            "away_team_logo": m.away_team.logo_url if m.away_team else None,
            "home_score": m.home_score,
            "away_score": m.away_score,
            "status": m.status,
            "match_date": m.match_date.isoformat(),
            "is_g3_vs_z3": m.is_g3_vs_z3,
        }

    return {
        "highlighted_matches": [serialize(m) for m in g3z3[:10] if m.status == "NS"],
        "live_matches": [serialize(m) for m in live],
        "recent_results": [serialize(m) for m in g3z3[:10] if m.status == "FT"],
    }
