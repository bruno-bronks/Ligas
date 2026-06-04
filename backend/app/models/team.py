"""Team model."""

from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.league import League


class Team(Base, TimestampMixin):
    """A football team."""

    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    short_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    code: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    api_football_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    league_id: Mapped[int] = mapped_column(ForeignKey("leagues.id"), nullable=False, index=True)
    logo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    venue: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    founded: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Relationships
    league: Mapped["League"] = relationship("League", back_populates="teams")

    def __repr__(self) -> str:
        return f"<Team {self.name} ({self.code})>"
