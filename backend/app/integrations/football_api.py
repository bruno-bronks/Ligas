"""
Football Intelligence Dashboard - API-Football Client
Async client for api-football.com (via api-sports.io).
Handles rate limiting, caching, and data transformation.
"""

from typing import Any, Dict, List, Optional

import httpx
from loguru import logger

from app.core.config import get_settings

settings = get_settings()


class APIFootballClient:
    """Client for the API-Football v3 API."""

    def __init__(self):
        self.base_url = settings.API_FOOTBALL_BASE_URL
        self.api_key = settings.API_FOOTBALL_KEY
        self.headers = {
            "x-apisports-key": self.api_key,
        }
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create the HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=self.headers,
                timeout=30.0,
                verify=False,
            )
        return self._client

    async def _request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a GET request to the API."""
        client = await self._get_client()
        try:
            response = await client.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            # Check API-level errors
            if data.get("errors"):
                logger.error(f"API-Football error: {data['errors']}")
                return {"response": []}

            # Log remaining requests
            remaining = data.get("paging", {})
            logger.debug(f"API-Football {endpoint}: {remaining}")

            return data
        except httpx.HTTPStatusError as e:
            logger.error(f"API-Football HTTP error {e.response.status_code}: {e}")
            return {"response": []}
        except Exception as e:
            logger.error(f"API-Football request error: {e}")
            return {"response": []}

    async def close(self):
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    # === League Endpoints ===

    async def get_leagues(self) -> List[Dict]:
        """Get all available leagues."""
        data = await self._request("/leagues")
        return data.get("response", [])

    async def get_league_info(self, league_id: int, season: int) -> Optional[Dict]:
        """Get specific league info."""
        data = await self._request("/leagues", {"id": league_id, "season": season})
        results = data.get("response", [])
        return results[0] if results else None

    # === Standings ===

    async def get_standings(self, league_id: int, season: int) -> List[Dict]:
        """Get league standings."""
        data = await self._request("/standings", {"league": league_id, "season": season})
        results = data.get("response", [])
        if results:
            standings = results[0].get("league", {}).get("standings", [[]])
            return standings[0] if standings else []
        return []

    # === Fixtures ===

    async def get_fixtures(
        self,
        league_id: int,
        season: int,
        status: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        last: Optional[int] = None,
        next_: Optional[int] = None,
    ) -> List[Dict]:
        """Get fixtures with optional filters."""
        params: Dict[str, Any] = {"league": league_id, "season": season}
        if status:
            params["status"] = status
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if last:
            params["last"] = last
        if next_:
            params["next"] = next_
        data = await self._request("/fixtures", params)
        return data.get("response", [])

    async def get_fixture_by_id(self, fixture_id: int) -> Optional[Dict]:
        """Get a specific fixture by ID."""
        data = await self._request("/fixtures", {"id": fixture_id})
        results = data.get("response", [])
        return results[0] if results else None

    # === Teams ===

    async def get_teams(self, league_id: int, season: int) -> List[Dict]:
        """Get all teams in a league."""
        data = await self._request("/teams", {"league": league_id, "season": season})
        return data.get("response", [])

    async def get_team_statistics(self, team_id: int, league_id: int, season: int) -> Optional[Dict]:
        """Get team statistics."""
        data = await self._request(
            "/teams/statistics",
            {"team": team_id, "league": league_id, "season": season},
        )
        return data.get("response") if data.get("response") else None

    # === Head to Head ===

    async def get_head_to_head(self, team1_id: int, team2_id: int, last: int = 10) -> List[Dict]:
        """Get head-to-head matches."""
        h2h = f"{team1_id}-{team2_id}"
        data = await self._request("/fixtures/headtohead", {"h2h": h2h, "last": last})
        return data.get("response", [])

    # === Top Scorers ===

    async def get_top_scorers(self, league_id: int, season: int) -> List[Dict]:
        """Get top scorers for a league."""
        data = await self._request("/players/topscorers", {"league": league_id, "season": season})
        return data.get("response", [])

    # === Predictions ===

    async def get_predictions(self, fixture_id: int) -> Optional[Dict]:
        """Get API predictions for a fixture."""
        data = await self._request("/predictions", {"fixture": fixture_id})
        results = data.get("response", [])
        return results[0] if results else None


# Singleton instance
api_football_client = APIFootballClient()
