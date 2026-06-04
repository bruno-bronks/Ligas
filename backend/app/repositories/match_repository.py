"""Match repository."""

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.match import Match
from app.repositories.base_repository import BaseRepository


class MatchRepository(BaseRepository[Match]):
    """Data access layer for matches."""

    def __init__(self, session: AsyncSession):
        super().__init__(Match, session)

    async def get_by_api_football_id(self, api_id: int) -> Optional[Match]:
        """Get match by API-Football ID."""
        result = await self.session.execute(
            select(Match).where(Match.api_football_id == api_id)
        )
        return result.scalar_one_or_none()

    async def get_by_season(
        self, season_id: int, status: Optional[str] = None, limit: int = 50
    ) -> List[Match]:
        """Get matches for a season, optionally filtered by status."""
        query = (
            select(Match)
            .options(joinedload(Match.home_team), joinedload(Match.away_team))
            .where(Match.season_id == season_id)
        )
        if status:
            query = query.where(Match.status == status)
        query = query.order_by(Match.match_date.desc()).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().unique().all())

    async def get_upcoming(self, season_id: int, limit: int = 20) -> List[Match]:
        """Get upcoming fixtures (not started)."""
        now = datetime.now(timezone.utc)
        result = await self.session.execute(
            select(Match)
            .options(joinedload(Match.home_team), joinedload(Match.away_team))
            .where(
                Match.season_id == season_id,
                Match.status == "NS",
                Match.match_date >= now,
            )
            .order_by(Match.match_date)
            .limit(limit)
        )
        return list(result.scalars().unique().all())

    async def get_recent_results(self, season_id: int, limit: int = 20) -> List[Match]:
        """Get recent finished matches."""
        result = await self.session.execute(
            select(Match)
            .options(joinedload(Match.home_team), joinedload(Match.away_team))
            .where(
                Match.season_id == season_id,
                Match.status == "FT",
            )
            .order_by(Match.match_date.desc())
            .limit(limit)
        )
        return list(result.scalars().unique().all())

    async def get_g3_vs_z3(self, season_id: Optional[int] = None) -> List[Match]:
        """Get all G3 vs Z3 matches."""
        query = (
            select(Match)
            .options(joinedload(Match.home_team), joinedload(Match.away_team))
            .where(Match.is_g3_vs_z3 == True)
        )
        if season_id:
            query = query.where(Match.season_id == season_id)
        query = query.order_by(Match.match_date.desc())
        result = await self.session.execute(query)
        return list(result.scalars().unique().all())

    async def get_team_matches(
        self, team_id: int, limit: int = 10
    ) -> List[Match]:
        """Get recent matches for a team."""
        result = await self.session.execute(
            select(Match)
            .options(joinedload(Match.home_team), joinedload(Match.away_team))
            .where(
                or_(Match.home_team_id == team_id, Match.away_team_id == team_id),
                Match.status == "FT",
            )
            .order_by(Match.match_date.desc())
            .limit(limit)
        )
        return list(result.scalars().unique().all())

    async def get_live_matches(self) -> List[Match]:
        """Get all currently live matches."""
        result = await self.session.execute(
            select(Match)
            .options(joinedload(Match.home_team), joinedload(Match.away_team))
            .where(Match.status.in_(["1H", "HT", "2H", "ET", "P"]))
            .order_by(Match.match_date)
        )
        return list(result.scalars().unique().all())

    async def get_match_detail(self, match_id: int) -> Optional[Match]:
        """Get match with all related data loaded."""
        result = await self.session.execute(
            select(Match)
            .options(
                joinedload(Match.home_team),
                joinedload(Match.away_team),
                joinedload(Match.prediction),
                joinedload(Match.ai_analysis),
                joinedload(Match.season),
            )
            .where(Match.id == match_id)
        )
        return result.scalar_one_or_none()
