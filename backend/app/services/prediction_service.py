"""
Football Intelligence Dashboard - Prediction Service
Statistical model for match outcome prediction.
"""

from typing import Dict, List, Optional, Tuple

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.match import Match
from app.models.prediction import Prediction
from app.models.standing import Standing
from app.repositories.match_repository import MatchRepository
from app.repositories.standing_repository import StandingRepository


class PredictionService:
    """Bayesian-weighted statistical prediction engine."""

    # Weight factors for the prediction model
    WEIGHTS = {
        "form_5": 0.20,       # Last 5 matches form
        "form_10": 0.15,      # Last 10 matches
        "h2h": 0.10,          # Head-to-head history
        "goals": 0.10,        # Goals scored/conceded
        "home_away": 0.15,    # Home/away performance
        "xg": 0.10,           # Expected goals
        "position": 0.10,     # League position
        "streak": 0.05,       # Win streak bonus
        "momentum": 0.05,     # Season momentum
    }

    def __init__(self, session: AsyncSession):
        self.session = session
        self.match_repo = MatchRepository(session)
        self.standing_repo = StandingRepository(session)

    async def predict_match(self, match: Match) -> Prediction:
        """Generate a prediction for a match."""
        home_team_id = match.home_team_id
        away_team_id = match.away_team_id
        season_id = match.season_id

        # Gather all inputs
        home_standing = await self.standing_repo.get_team_standing(season_id, home_team_id)
        away_standing = await self.standing_repo.get_team_standing(season_id, away_team_id)

        home_matches = await self.match_repo.get_team_matches(home_team_id, limit=10)
        away_matches = await self.match_repo.get_team_matches(away_team_id, limit=10)

        # Calculate component scores
        home_score = 0.5  # Base probability
        away_score = 0.5

        # 1. League position factor
        if home_standing and away_standing:
            pos_factor = self._position_factor(home_standing.position, away_standing.position)
            home_score += pos_factor * self.WEIGHTS["position"]
            away_score -= pos_factor * self.WEIGHTS["position"]

        # 2. Form factor (last 5)
        if home_standing and home_standing.form:
            home_form = self._form_score(home_standing.form[-5:])
            home_score += home_form * self.WEIGHTS["form_5"]
        if away_standing and away_standing.form:
            away_form = self._form_score(away_standing.form[-5:])
            away_score += away_form * self.WEIGHTS["form_5"]

        # 3. Home/away advantage
        if home_standing and away_standing:
            ha_factor = self._home_away_factor(home_standing, away_standing)
            home_score += ha_factor * self.WEIGHTS["home_away"]
            away_score -= ha_factor * self.WEIGHTS["home_away"]

        # 4. Goals factor
        if home_standing and away_standing:
            goals_factor = self._goals_factor(home_standing, away_standing)
            home_score += goals_factor * self.WEIGHTS["goals"]
            away_score -= goals_factor * self.WEIGHTS["goals"]

        # 5. Points factor
        if home_standing and away_standing:
            pts_factor = self._points_factor(home_standing.points, away_standing.points)
            home_score += pts_factor * self.WEIGHTS["form_10"]
            away_score -= pts_factor * self.WEIGHTS["form_10"]

        # Normalize to probabilities
        home_prob, draw_prob, away_prob = self._normalize_probabilities(
            home_score, away_score
        )

        # Over 2.5 and BTTS
        over_2_5 = self._calc_over_2_5(home_standing, away_standing)
        btts = self._calc_btts(home_standing, away_standing)

        # Build model inputs for transparency
        model_inputs = {
            "home_position": home_standing.position if home_standing else None,
            "away_position": away_standing.position if away_standing else None,
            "home_form": home_standing.form if home_standing else None,
            "away_form": away_standing.form if away_standing else None,
            "home_points": home_standing.points if home_standing else None,
            "away_points": away_standing.points if away_standing else None,
            "raw_home_score": round(home_score, 4),
            "raw_away_score": round(away_score, 4),
        }

        prediction = Prediction(
            match_id=match.id,
            home_win_prob=round(home_prob, 4),
            draw_prob=round(draw_prob, 4),
            away_win_prob=round(away_prob, 4),
            over_2_5_prob=round(over_2_5, 4) if over_2_5 else None,
            btts_prob=round(btts, 4) if btts else None,
            model_inputs=model_inputs,
            model_version="v1.0-bayesian",
        )

        return prediction

    def _position_factor(self, home_pos: int, away_pos: int) -> float:
        """Position-based advantage. Returns -0.3 to 0.3."""
        diff = away_pos - home_pos  # positive = home is better
        return max(-0.3, min(0.3, diff * 0.015))

    def _form_score(self, form: str) -> float:
        """Convert form string to score. W=1, D=0.3, L=-0.2. Returns -0.2 to 0.3."""
        scores = {"W": 1.0, "D": 0.3, "L": -0.2}
        if not form:
            return 0
        total = sum(scores.get(c, 0) for c in form)
        return max(-0.2, min(0.3, total / len(form) * 0.3))

    def _home_away_factor(self, home_standing: Standing, away_standing: Standing) -> float:
        """Home/away performance advantage."""
        home_home_ratio = (
            home_standing.home_won / max(1, home_standing.home_played)
        )
        away_away_ratio = (
            away_standing.away_won / max(1, away_standing.away_played)
        )
        return max(-0.2, min(0.2, (home_home_ratio - away_away_ratio) * 0.3))

    def _goals_factor(self, home_standing: Standing, away_standing: Standing) -> float:
        """Goal scoring/conceding advantage."""
        home_gd_per_game = home_standing.goal_difference / max(1, home_standing.played)
        away_gd_per_game = away_standing.goal_difference / max(1, away_standing.played)
        return max(-0.2, min(0.2, (home_gd_per_game - away_gd_per_game) * 0.1))

    def _points_factor(self, home_pts: int, away_pts: int) -> float:
        """Points-based advantage."""
        diff = home_pts - away_pts
        return max(-0.2, min(0.2, diff * 0.005))

    def _normalize_probabilities(
        self, home_score: float, away_score: float
    ) -> Tuple[float, float, float]:
        """Normalize raw scores to probabilities summing to 1.0."""
        # Home advantage bonus
        home_score += 0.08

        # Clamp
        home_score = max(0.05, min(0.95, home_score))
        away_score = max(0.05, min(0.95, away_score))

        # Draw probability increases when teams are close
        score_diff = abs(home_score - away_score)
        draw_base = max(0.15, 0.35 - score_diff)

        # Distribute remaining probability
        remaining = 1.0 - draw_base
        total = home_score + away_score
        home_prob = (home_score / total) * remaining
        away_prob = (away_score / total) * remaining

        return home_prob, draw_base, away_prob

    def _calc_over_2_5(
        self, home: Optional[Standing], away: Optional[Standing]
    ) -> Optional[float]:
        """Calculate probability of over 2.5 goals."""
        if not home or not away:
            return None
        home_avg = (home.goals_for + home.goals_against) / max(1, home.played)
        away_avg = (away.goals_for + away.goals_against) / max(1, away.played)
        combined = (home_avg + away_avg) / 2
        return min(0.95, max(0.1, (combined - 2.0) * 0.4 + 0.5))

    def _calc_btts(
        self, home: Optional[Standing], away: Optional[Standing]
    ) -> Optional[float]:
        """Calculate probability of both teams scoring."""
        if not home or not away:
            return None
        home_scores = home.goals_for / max(1, home.played)
        away_scores = away.goals_for / max(1, away.played)
        home_concedes = home.goals_against / max(1, home.played)
        away_concedes = away.goals_against / max(1, away.played)

        prob = (min(home_scores, away_concedes) + min(away_scores, home_concedes)) / 4
        return min(0.9, max(0.1, prob + 0.3))
