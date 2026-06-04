"""Prediction model."""

from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.match import Match


class Prediction(Base, TimestampMixin):
    """Match prediction with probabilities."""

    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"), unique=True, nullable=False, index=True)
    home_win_prob: Mapped[float] = mapped_column(Float, nullable=False)
    draw_prob: Mapped[float] = mapped_column(Float, nullable=False)
    away_win_prob: Mapped[float] = mapped_column(Float, nullable=False)
    over_2_5_prob: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    btts_prob: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # Both teams to score
    model_inputs: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    model_version: Mapped[str] = mapped_column(String(50), default="v1.0")

    # Relationships
    match: Mapped["Match"] = relationship("Match", back_populates="prediction")

    @property
    def predicted_outcome(self) -> str:
        """Return the most likely outcome."""
        probs = {
            "home": self.home_win_prob,
            "draw": self.draw_prob,
            "away": self.away_win_prob,
        }
        return max(probs, key=probs.get)

    def __repr__(self) -> str:
        return f"<Prediction Match#{self.match_id}: H={self.home_win_prob:.0%} D={self.draw_prob:.0%} A={self.away_win_prob:.0%}>"
