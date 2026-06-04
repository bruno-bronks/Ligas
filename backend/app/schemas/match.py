"""Match schemas."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class MatchResponse(BaseModel):
    """Match summary."""
    id: int
    season_id: int
    home_team_id: int
    away_team_id: int
    home_team_name: str
    away_team_name: str
    home_team_logo: Optional[str] = None
    away_team_logo: Optional[str] = None
    league_code: str
    league_name: str
    matchday: Optional[int] = None
    match_date: datetime
    status: str
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    venue: Optional[str] = None
    is_g3_vs_z3: bool = False

    model_config = {"from_attributes": True}


class HeadToHeadSummary(BaseModel):
    """H2H summary between two teams."""
    total_matches: int = 0
    team1_wins: int = 0
    team2_wins: int = 0
    draws: int = 0
    total_goals: int = 0
    last_matches: Optional[list] = None


class PredictionSummary(BaseModel):
    """Prediction summary for a match."""
    home_win_prob: float
    draw_prob: float
    away_win_prob: float
    over_2_5_prob: Optional[float] = None
    btts_prob: Optional[float] = None
    predicted_outcome: str


class MatchDetailResponse(MatchResponse):
    """Match with full details."""
    home_ht_score: Optional[int] = None
    away_ht_score: Optional[int] = None
    home_xg: Optional[float] = None
    away_xg: Optional[float] = None
    referee: Optional[str] = None
    head_to_head: Optional[HeadToHeadSummary] = None
    prediction: Optional[PredictionSummary] = None
    ai_analysis: Optional[str] = None


class MatchListResponse(BaseModel):
    """Paginated match list."""
    matches: List[MatchResponse]
    total: int
    page: int = 1
    per_page: int = 20


class G3vsZ3Response(BaseModel):
    """G3 vs Z3 highlighted matches."""
    upcoming: List[MatchResponse]
    recent: List[MatchResponse]
    total: int
