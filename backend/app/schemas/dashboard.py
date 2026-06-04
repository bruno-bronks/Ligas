"""Dashboard schemas."""

from typing import List, Optional

from pydantic import BaseModel

from app.schemas.match import MatchResponse


class LeagueSummaryWidget(BaseModel):
    """Compact league info for dashboard."""
    code: str
    name: str
    country: str
    flag_emoji: Optional[str] = None
    leader_team: Optional[str] = None
    leader_points: Optional[int] = None
    matches_played: int = 0
    total_goals: int = 0


class TopScoringTeam(BaseModel):
    """Top scoring team widget data."""
    team_name: str
    team_logo: Optional[str] = None
    league_code: str
    goals: int
    matches: int
    avg_goals: float


class DashboardOverviewResponse(BaseModel):
    """Dashboard aggregate data."""
    total_leagues: int
    total_teams: int
    total_matches: int
    total_goals: int
    leagues: List[LeagueSummaryWidget]
    top_scoring_teams: List[TopScoringTeam]
    upcoming_g3_vs_z3: int


class DashboardHighlightsResponse(BaseModel):
    """Dashboard highlighted matches."""
    highlighted_matches: List[MatchResponse]
    live_matches: List[MatchResponse]
    recent_results: List[MatchResponse]
