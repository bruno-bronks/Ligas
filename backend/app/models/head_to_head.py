"""Head-to-head record model."""

from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.team import Team


class HeadToHead(Base, TimestampMixin):
    """Historical head-to-head record between two teams."""

    __tablename__ = "head_to_head"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team1_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False, index=True)
    team2_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False, index=True)
    total_matches: Mapped[int] = mapped_column(Integer, default=0)
    team1_wins: Mapped[int] = mapped_column(Integer, default=0)
    team2_wins: Mapped[int] = mapped_column(Integer, default=0)
    draws: Mapped[int] = mapped_column(Integer, default=0)
    total_goals: Mapped[int] = mapped_column(Integer, default=0)
    last_matches: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)  # Last N encounters

    # Relationships
    team1: Mapped["Team"] = relationship("Team", foreign_keys=[team1_id])
    team2: Mapped["Team"] = relationship("Team", foreign_keys=[team2_id])

    def __repr__(self) -> str:
        return f"<H2H Team#{self.team1_id} vs Team#{self.team2_id}: {self.total_matches} matches>"
