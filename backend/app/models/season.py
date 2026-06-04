"""Season model."""

from typing import TYPE_CHECKING, List, Optional
from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.league import League
    from app.models.match import Match
    from app.models.standing import Standing


class Season(Base, TimestampMixin):
    """A season within a league (e.g., 2024-2025)."""

    __tablename__ = "seasons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    league_id: Mapped[int] = mapped_column(ForeignKey("leagues.id"), nullable=False, index=True)
    year: Mapped[str] = mapped_column(String(10), nullable=False)  # e.g., "2024"
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    league: Mapped["League"] = relationship("League", back_populates="seasons")
    standings: Mapped[List["Standing"]] = relationship("Standing", back_populates="season", cascade="all, delete-orphan")
    matches: Mapped[List["Match"]] = relationship("Match", back_populates="season", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Season {self.year} - League #{self.league_id}>"
