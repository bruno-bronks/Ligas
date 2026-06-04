"""Standing schemas."""

from typing import List, Optional

from pydantic import BaseModel


class StandingResponse(BaseModel):
    """Single standing row."""
    position: int
    team_id: int
    team_name: str
    team_logo: Optional[str] = None
    played: int
    won: int
    drawn: int
    lost: int
    goals_for: int
    goals_against: int
    goal_difference: int
    points: int
    form: Optional[str] = None
    description: Optional[str] = None

    # Home/Away splits
    home_played: int = 0
    home_won: int = 0
    home_drawn: int = 0
    home_lost: int = 0
    home_goals_for: int = 0
    home_goals_against: int = 0

    away_played: int = 0
    away_won: int = 0
    away_drawn: int = 0
    away_lost: int = 0
    away_goals_for: int = 0
    away_goals_against: int = 0

    model_config = {"from_attributes": True}


class StandingsTableResponse(BaseModel):
    """Full standings table for a league."""
    league_code: str
    league_name: str
    season_year: str
    standings: List[StandingResponse]
    g3_teams: List[int] = []  # team_ids in top 3
    z3_teams: List[int] = []  # team_ids in bottom 3
