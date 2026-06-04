"""League repository."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.league import League
from app.repositories.base_repository import BaseRepository


class LeagueRepository(BaseRepository[League]):
    """Data access layer for leagues."""

    def __init__(self, session: AsyncSession):
        super().__init__(League, session)

    async def get_by_code(self, code: str) -> Optional[League]:
        """Get a league by its code."""
        result = await self.session.execute(
            select(League).where(League.code == code)
        )
        return result.scalar_one_or_none()

    async def get_by_api_football_id(self, api_id: int) -> Optional[League]:
        """Get a league by its API-Football ID."""
        result = await self.session.execute(
            select(League).where(League.api_football_id == api_id)
        )
        return result.scalar_one_or_none()

    async def get_all_active(self) -> List[League]:
        """Get all active leagues."""
        result = await self.session.execute(
            select(League)
            .where(League.is_active == True)
            .order_by(League.country)
        )
        return list(result.scalars().all())

    async def get_with_seasons(self, code: str) -> Optional[League]:
        """Get league with all seasons loaded."""
        result = await self.session.execute(
            select(League)
            .options(selectinload(League.seasons))
            .where(League.code == code)
        )
        return result.scalar_one_or_none()

    async def get_with_teams(self, code: str) -> Optional[League]:
        """Get league with all teams loaded."""
        result = await self.session.execute(
            select(League)
            .options(selectinload(League.teams))
            .where(League.code == code)
        )
        return result.scalar_one_or_none()
