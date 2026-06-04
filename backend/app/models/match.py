"""Match model."""

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.ai_analysis import AIAnalysis
    from app.models.notification_log import NotificationLog
    from app.models.prediction import Prediction
    from app.models.season import Season
    from app.models.team import Team


class Match(Base, TimestampMixin):
    """A football match / fixture."""

    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id"), nullable=False, index=True)
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False, index=True)
    away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False, index=True)
    api_football_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    matchday: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    match_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="NS")  # NS, 1H, HT, 2H, FT, etc.
    home_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    away_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    home_ht_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    away_ht_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    home_xg: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    away_xg: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    venue: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    referee: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    is_g3_vs_z3: Mapped[bool] = mapped_column(Boolean, default=False, index=True)

    # Relationships
    season: Mapped["Season"] = relationship("Season", back_populates="matches")
    home_team: Mapped["Team"] = relationship("Team", foreign_keys=[home_team_id])
    away_team: Mapped["Team"] = relationship("Team", foreign_keys=[away_team_id])
    prediction: Mapped[Optional["Prediction"]] = relationship(
        "Prediction", back_populates="match", uselist=False, cascade="all, delete-orphan"
    )
    ai_analysis: Mapped[Optional["AIAnalysis"]] = relationship(
        "AIAnalysis", back_populates="match", uselist=False, cascade="all, delete-orphan"
    )
    notification_logs: Mapped[List["NotificationLog"]] = relationship(
        "NotificationLog", back_populates="match", cascade="all, delete-orphan"
    )

    @property
    def is_finished(self) -> bool:
        return self.status == "FT"

    @property
    def is_live(self) -> bool:
        return self.status in ("1H", "HT", "2H", "ET", "P")

    @property
    def score_display(self) -> str:
        if self.home_score is not None and self.away_score is not None:
            return f"{self.home_score} - {self.away_score}"
        return "vs"

    def __repr__(self) -> str:
        return f"<Match {self.id}: Home#{self.home_team_id} {self.score_display} Away#{self.away_team_id}>"
