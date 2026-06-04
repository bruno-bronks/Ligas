"""Team repository."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.team import Team
from app.repositories.base_repository import BaseRepository


class TeamRepository(BaseRepository[Team]):
    """Data access layer for teams."""

    def __init__(self, session: AsyncSession):
        super().__init__(Team, session)

    async def get_by_api_football_id(self, api_id: int) -> Optional[Team]:
        """Get team by API-Football ID."""
        result = await self.session.execute(
            select(Team).where(Team.api_football_id == api_id)
        )
        return result.scalar_one_or_none()

    async def get_by_league(self, league_id: int) -> List[Team]:
        """Get all teams in a league."""
        result = await self.session.execute(
            select(Team)
            .where(Team.league_id == league_id)
            .order_by(Team.name)
        )
        return list(result.scalars().all())

    async def search_by_name(self, query: str, limit: int = 20) -> List[Team]:
        """Search teams by name (case-insensitive)."""
        result = await self.session.execute(
            select(Team)
            .where(Team.name.ilike(f"%{query}%"))
            .order_by(Team.name)
            .limit(limit)
        )
        return list(result.scalars().all())
