"""AI Analysis model."""

from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.match import Match


class AIAnalysis(Base, TimestampMixin):
    """LLM-generated match analysis."""

    __tablename__ = "ai_analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"), unique=True, nullable=False, index=True)
    analysis_text: Mapped[str] = mapped_column(Text, nullable=False)
    llm_provider: Mapped[str] = mapped_column(String(50), nullable=False)  # "openai" or "gemini"
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g., "gpt-4o", "gemini-pro"
    analysis_sections: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)

    # Relationships
    match: Mapped["Match"] = relationship("Match", back_populates="ai_analysis")

    def __repr__(self) -> str:
        return f"<AIAnalysis Match#{self.match_id} via {self.llm_provider}/{self.model_name}>"
