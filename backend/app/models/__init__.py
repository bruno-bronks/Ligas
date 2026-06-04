"""
Football Intelligence Dashboard - ORM Models
All SQLAlchemy models for the football analytics platform.
"""

from app.models.league import League
from app.models.season import Season
from app.models.team import Team
from app.models.standing import Standing
from app.models.match import Match
from app.models.head_to_head import HeadToHead
from app.models.prediction import Prediction
from app.models.ai_analysis import AIAnalysis
from app.models.notification_log import NotificationLog
from app.models.user import User

__all__ = [
    "League",
    "Season",
    "Team",
    "Standing",
    "Match",
    "HeadToHead",
    "Prediction",
    "AIAnalysis",
    "NotificationLog",
    "User",
]
