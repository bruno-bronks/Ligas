"""Team schemas."""

from typing import List, Optional

from pydantic import BaseModel


class TeamResponse(BaseModel):
    """Team response."""
    id: int
    name: str
    short_name: Optional[str] = None
    code: Optional[str] = None
    api_football_id: int
    league_id: int
    logo_url: Optional[str] = None
    venue: Optional[str] = None
    founded: Optional[int] = None

    model_config = {"from_attributes": True}


class TeamWithStatsResponse(TeamResponse):
    """Team with current season stats."""
    position: Optional[int] = None
    points: Optional[int] = None
    played: Optional[int] = None
    won: Optional[int] = None
    drawn: Optional[int] = None
    lost: Optional[int] = None
    goals_for: Optional[int] = None
    goals_against: Optional[int] = None
    form: Optional[str] = None


class TeamSearchResponse(BaseModel):
    """Team search results."""
    teams: List[TeamResponse]
    total: int


class TeamFormResponse(BaseModel):
    """Team's recent form."""
    team: TeamResponse
    form: str
    last_matches: List[dict]
