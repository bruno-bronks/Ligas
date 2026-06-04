"""AI Analysis schemas."""

from typing import Any, Optional

from pydantic import BaseModel


class AIAnalysisResponse(BaseModel):
    """AI analysis response."""
    id: int
    match_id: int
    analysis_text: str
    llm_provider: str
    model_name: str
    analysis_sections: Optional[Any] = None

    model_config = {"from_attributes": True}
