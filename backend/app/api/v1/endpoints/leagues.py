"""
League API endpoints.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.league import League
from app.models.season import Season
from app.models.standing import Standing
from app.models.team import Team
from app.repositories.league_repository import LeagueRepository
from app.repositories.standing_repository import StandingRepository
from app.schemas.league import LeagueResponse, LeagueListResponse, LeagueDetailResponse, SeasonSummary
from app.schemas.standing import StandingResponse, StandingsTableResponse

router = APIRouter()


@router.get("", response_model=LeagueListResponse)
async def list_leagues(db: AsyncSession = Depends(get_db)):
    """List all active leagues."""
    repo = LeagueRepository(db)
    leagues = await repo.get_all_active()
    return LeagueListResponse(
        leagues=[LeagueResponse.model_validate(l) for l in leagues],
        total=len(leagues),
    )


@router.get("/{code}", response_model=LeagueDetailResponse)
async def get_league(code: str, db: AsyncSession = Depends(get_db)):
    """Get league details with seasons."""
    repo = LeagueRepository(db)
    league = await repo.get_with_seasons(code.upper())
    if not league:
        raise HTTPException(status_code=404, detail=f"League '{code}' not found")

    # Count teams
    result = await db.execute(
        select(Team).where(Team.league_id == league.id)
    )
    teams = result.scalars().all()

    # Find current season
    current_season = next((s for s in league.seasons if s.is_current), None)

    return LeagueDetailResponse(
        **LeagueResponse.model_validate(league).model_dump(),
        seasons=[SeasonSummary.model_validate(s) for s in league.seasons],
        current_season=SeasonSummary.model_validate(current_season) if current_season else None,
        total_teams=len(list(teams)),
    )


@router.get("/{code}/standings", response_model=StandingsTableResponse)
async def get_standings(code: str, db: AsyncSession = Depends(get_db)):
    """Get league standings."""
    league_repo = LeagueRepository(db)
    league = await league_repo.get_by_code(code.upper())
    if not league:
        raise HTTPException(status_code=404, detail=f"League '{code}' not found")

    # Find current season
    result = await db.execute(
        select(Season)
        .where(Season.league_id == league.id, Season.is_current == True)
        .order_by(Season.year.desc())
        .limit(1)
    )
    season = result.scalars().first()
    if not season:
        return StandingsTableResponse(
            league_code=code, league_name=league.name,
            season_year="N/A", standings=[]
        )

    standing_repo = StandingRepository(db)
    standings = await standing_repo.get_by_season(season.id)

    standing_responses = []
    for s in standings:
        standing_responses.append(StandingResponse(
            position=s.position,
            team_id=s.team_id,
            team_name=s.team.name if s.team else "Unknown",
            team_logo=s.team.logo_url if s.team else None,
            played=s.played, won=s.won, drawn=s.drawn, lost=s.lost,
            goals_for=s.goals_for, goals_against=s.goals_against,
            goal_difference=s.goal_difference, points=s.points,
            form=s.form, description=s.description,
            home_played=s.home_played, home_won=s.home_won,
            home_drawn=s.home_drawn, home_lost=s.home_lost,
            home_goals_for=s.home_goals_for, home_goals_against=s.home_goals_against,
            away_played=s.away_played, away_won=s.away_won,
            away_drawn=s.away_drawn, away_lost=s.away_lost,
            away_goals_for=s.away_goals_for, away_goals_against=s.away_goals_against,
        ))

    g3 = [s.team_id for s in standings[:3]]
    z3 = [s.team_id for s in standings[-3:]] if len(standings) >= 6 else []

    return StandingsTableResponse(
        league_code=code,
        league_name=league.name,
        season_year=season.year,
        standings=standing_responses,
        g3_teams=g3,
        z3_teams=z3,
    )


@router.get("/{code}/fixtures")
async def get_fixtures(code: str, db: AsyncSession = Depends(get_db)):
    """Get upcoming fixtures for a league."""
    from app.repositories.match_repository import MatchRepository

    league_repo = LeagueRepository(db)
    league = await league_repo.get_by_code(code.upper())
    if not league:
        raise HTTPException(status_code=404, detail=f"League '{code}' not found")

    result = await db.execute(
        select(Season)
        .where(Season.league_id == league.id, Season.is_current == True)
        .order_by(Season.year.desc())
        .limit(1)
    )
    season = result.scalars().first()
    if not season:
        return {"fixtures": [], "total": 0}

    match_repo = MatchRepository(db)
    fixtures = await match_repo.get_upcoming(season.id)

    return {
        "fixtures": [
            {
                "id": m.id,
                "home_team": m.home_team.name if m.home_team else "?",
                "away_team": m.away_team.name if m.away_team else "?",
                "home_team_logo": m.home_team.logo_url if m.home_team else None,
                "away_team_logo": m.away_team.logo_url if m.away_team else None,
                "match_date": m.match_date.isoformat(),
                "matchday": m.matchday,
                "venue": m.venue,
                "is_g3_vs_z3": m.is_g3_vs_z3,
            }
            for m in fixtures
        ],
        "total": len(fixtures),
    }


@router.get("/{code}/results")
async def get_results(code: str, limit: int = 20, db: AsyncSession = Depends(get_db)):
    """Get recent results for a league."""
    from app.repositories.match_repository import MatchRepository

    league_repo = LeagueRepository(db)
    league = await league_repo.get_by_code(code.upper())
    if not league:
        raise HTTPException(status_code=404, detail=f"League '{code}' not found")

    result = await db.execute(
        select(Season)
        .where(Season.league_id == league.id, Season.is_current == True)
        .order_by(Season.year.desc())
        .limit(1)
    )
    season = result.scalars().first()
    if not season:
        return {"results": [], "total": 0}

    match_repo = MatchRepository(db)
    results_list = await match_repo.get_recent_results(season.id, limit=limit)

    return {
        "results": [
            {
                "id": m.id,
                "home_team": m.home_team.name if m.home_team else "?",
                "away_team": m.away_team.name if m.away_team else "?",
                "home_team_logo": m.home_team.logo_url if m.home_team else None,
                "away_team_logo": m.away_team.logo_url if m.away_team else None,
                "home_score": m.home_score,
                "away_score": m.away_score,
                "match_date": m.match_date.isoformat(),
                "matchday": m.matchday,
                "is_g3_vs_z3": m.is_g3_vs_z3,
            }
            for m in results_list
        ],
        "total": len(results_list),
    }
