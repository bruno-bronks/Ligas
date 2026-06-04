"""Pydantic schemas for API request/response."""

from app.schemas.league import LeagueResponse, LeagueListResponse, LeagueDetailResponse
from app.schemas.team import TeamResponse, TeamSearchResponse
from app.schemas.standing import StandingResponse, StandingsTableResponse
from app.schemas.match import MatchResponse, MatchDetailResponse, MatchListResponse, G3vsZ3Response
from app.schemas.prediction import PredictionResponse
from app.schemas.analysis import AIAnalysisResponse
from app.schemas.dashboard import DashboardOverviewResponse, DashboardHighlightsResponse
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse

__all__ = [
    "LeagueResponse", "LeagueListResponse", "LeagueDetailResponse",
    "TeamResponse", "TeamSearchResponse",
    "StandingResponse", "StandingsTableResponse",
    "MatchResponse", "MatchDetailResponse", "MatchListResponse", "G3vsZ3Response",
    "PredictionResponse",
    "AIAnalysisResponse",
    "DashboardOverviewResponse", "DashboardHighlightsResponse",
    "LoginRequest", "RegisterRequest", "TokenResponse", "UserResponse",
]
