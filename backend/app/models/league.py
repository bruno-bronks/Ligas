"""League model."""

from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.season import Season
    from app.models.team import Team


class League(Base, TimestampMixin):
    """Football league (e.g., Premier League, La Liga)."""

    __tablename__ = "leagues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    api_football_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    logo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    flag_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    flag_emoji: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    seasons: Mapped[List["Season"]] = relationship("Season", back_populates="league", cascade="all, delete-orphan")
    teams: Mapped[List["Team"]] = relationship("Team", back_populates="league", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<League {self.flag_emoji} {self.name} ({self.country})>"
