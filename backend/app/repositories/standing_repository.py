"""Standing repository."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.standing import Standing
from app.repositories.base_repository import BaseRepository


class StandingRepository(BaseRepository[Standing]):
    """Data access layer for standings."""

    def __init__(self, session: AsyncSession):
        super().__init__(Standing, session)

    async def get_by_season(self, season_id: int) -> List[Standing]:
        """Get all standings for a season, ordered by position."""
        result = await self.session.execute(
            select(Standing)
            .options(joinedload(Standing.team))
            .where(Standing.season_id == season_id)
            .order_by(Standing.position)
        )
        return list(result.scalars().unique().all())

    async def get_team_standing(self, season_id: int, team_id: int) -> Optional[Standing]:
        """Get a specific team's standing."""
        result = await self.session.execute(
            select(Standing)
            .where(Standing.season_id == season_id, Standing.team_id == team_id)
        )
        return result.scalar_one_or_none()

    async def get_g3_teams(self, season_id: int) -> List[Standing]:
        """Get top 3 teams (G3)."""
        result = await self.session.execute(
            select(Standing)
            .options(joinedload(Standing.team))
            .where(Standing.season_id == season_id)
            .order_by(Standing.position)
            .limit(3)
        )
        return list(result.scalars().unique().all())

    async def get_z3_teams(self, season_id: int) -> List[Standing]:
        """Get bottom 3 teams (Z3)."""
        result = await self.session.execute(
            select(Standing)
            .options(joinedload(Standing.team))
            .where(Standing.season_id == season_id)
            .order_by(Standing.position.desc())
            .limit(3)
        )
        return list(result.scalars().unique().all())

    async def upsert(self, season_id: int, team_id: int, data: dict) -> Standing:
        """Insert or update a standing record."""
        existing = await self.get_team_standing(season_id, team_id)
        if existing:
            for key, value in data.items():
                setattr(existing, key, value)
            return await self.update(existing)
        else:
            standing = Standing(season_id=season_id, team_id=team_id, **data)
            return await self.create(standing)
