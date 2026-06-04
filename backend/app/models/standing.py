"""Standing model."""

from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.season import Season
    from app.models.team import Team


class Standing(Base, TimestampMixin):
    """League standings / classification table."""

    __tablename__ = "standings"
    __table_args__ = (
        UniqueConstraint("season_id", "team_id", name="uq_standing_season_team"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id"), nullable=False, index=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False, index=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    played: Mapped[int] = mapped_column(Integer, default=0)
    won: Mapped[int] = mapped_column(Integer, default=0)
    drawn: Mapped[int] = mapped_column(Integer, default=0)
    lost: Mapped[int] = mapped_column(Integer, default=0)
    goals_for: Mapped[int] = mapped_column(Integer, default=0)
    goals_against: Mapped[int] = mapped_column(Integer, default=0)
    goal_difference: Mapped[int] = mapped_column(Integer, default=0)
    points: Mapped[int] = mapped_column(Integer, default=0)
    form: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # e.g., "WWDLW"
    description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)  # e.g., "Champions League"

    # Home/Away split
    home_played: Mapped[int] = mapped_column(Integer, default=0)
    home_won: Mapped[int] = mapped_column(Integer, default=0)
    home_drawn: Mapped[int] = mapped_column(Integer, default=0)
    home_lost: Mapped[int] = mapped_column(Integer, default=0)
    home_goals_for: Mapped[int] = mapped_column(Integer, default=0)
    home_goals_against: Mapped[int] = mapped_column(Integer, default=0)

    away_played: Mapped[int] = mapped_column(Integer, default=0)
    away_won: Mapped[int] = mapped_column(Integer, default=0)
    away_drawn: Mapped[int] = mapped_column(Integer, default=0)
    away_lost: Mapped[int] = mapped_column(Integer, default=0)
    away_goals_for: Mapped[int] = mapped_column(Integer, default=0)
    away_goals_against: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    season: Mapped["Season"] = relationship("Season", back_populates="standings")
    team: Mapped["Team"] = relationship("Team")

    def __repr__(self) -> str:
        return f"<Standing #{self.position} {self.points}pts>"
