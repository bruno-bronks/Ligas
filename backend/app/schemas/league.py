"""League schemas."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class LeagueResponse(BaseModel):
    """League summary response."""
    id: int
    name: str
    country: str
    code: str
    api_football_id: int
    logo_url: Optional[str] = None
    flag_url: Optional[str] = None
    flag_emoji: Optional[str] = None
    is_active: bool = True

    model_config = {"from_attributes": True}


class SeasonSummary(BaseModel):
    """Brief season info."""
    id: int
    year: str
    is_current: bool

    model_config = {"from_attributes": True}


class LeagueListResponse(BaseModel):
    """List of all leagues."""
    leagues: List[LeagueResponse]
    total: int


class LeagueDetailResponse(LeagueResponse):
    """League with seasons and stats."""
    seasons: List[SeasonSummary] = []
    current_season: Optional[SeasonSummary] = None
    total_teams: int = 0
