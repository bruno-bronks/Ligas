"""Prediction schemas."""

from typing import Any, Optional

from pydantic import BaseModel


class PredictionResponse(BaseModel):
    """Full prediction response."""
    id: int
    match_id: int
    home_win_prob: float
    draw_prob: float
    away_win_prob: float
    over_2_5_prob: Optional[float] = None
    btts_prob: Optional[float] = None
    model_inputs: Optional[Any] = None
    model_version: str = "v1.0"
    predicted_outcome: str

    model_config = {"from_attributes": True}
