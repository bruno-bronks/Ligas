"""
Team API endpoints.
"""

import hashlib
import os
import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response, FileResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.match_repository import MatchRepository
from app.repositories.team_repository import TeamRepository
from app.schemas.team import TeamResponse, TeamSearchResponse

router = APIRouter()

# Directory to cache logos locally.
CACHE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
    "data",
    "logo_cache"
)

DEFAULT_SHIELD_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 120" width="100" height="120">
  <path d="M50 10 L90 25 L90 65 C90 95 50 115 50 115 C50 115 10 95 10 65 L10 25 Z" fill="#1e293b" stroke="#64748b" stroke-width="4" />
  <path d="M50 20 L80 32 L80 65 C80 88 50 102 50 102 C50 102 20 88 20 65 L20 32 Z" fill="#0f172a" />
  <circle cx="50" cy="55" r="18" fill="none" stroke="#3b82f6" stroke-width="4" stroke-dasharray="8,4" />
  <path d="M50 42 L60 55 L40 55 Z" fill="#10b981" />
  <circle cx="50" cy="72" r="4" fill="#3b82f6" />
</svg>"""


@router.get("/logo-proxy")
async def logo_proxy(url: str = Query(..., description="The original logo URL from api-sports")):
    """Proxy and cache team/league logos to bypass DNS resolution issues."""
    if not url.startswith("http"):
        raise HTTPException(status_code=400, detail="Invalid URL")

    # Extract extension and hash the URL to generate a unique cache filename
    url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()
    
    # Determine correct file extension
    ext = "png"
    if url.endswith(".jpg") or url.endswith(".jpeg"):
        ext = "jpg"
    elif url.endswith(".svg"):
        ext = "svg"
    
    filename = f"{url_hash}.{ext}"
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, filename)

    # Check local cache first
    if os.path.exists(cache_path):
        return FileResponse(cache_path, media_type=f"image/{ext}")

    # Fetch from remote server using patched DNS resolving and verifying=False
    try:
        async with httpx.AsyncClient(verify=False, timeout=8.0) as client:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            }
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                with open(cache_path, "wb") as f:
                    f.write(response.content)
                return Response(
                    content=response.content,
                    media_type=response.headers.get("content-type", f"image/{ext}")
                )
            else:
                logger.warning(f"Failed to fetch team logo, remote returned status {response.status_code} for {url}")
    except Exception as e:
        logger.error(f"Error fetching team logo from remote {url}: {e}")

    # Return fallback default shield SVG if remote fetch fails
    return Response(content=DEFAULT_SHIELD_SVG, media_type="image/svg+xml")



@router.get("/search", response_model=TeamSearchResponse)
async def search_teams(q: str, limit: int = 20, db: AsyncSession = Depends(get_db)):
    """Search teams by name."""
    repo = TeamRepository(db)
    teams = await repo.search_by_name(q, limit=limit)
    return TeamSearchResponse(
        teams=[TeamResponse.model_validate(t) for t in teams],
        total=len(teams),
    )


@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(team_id: int, db: AsyncSession = Depends(get_db)):
    """Get team details."""
    repo = TeamRepository(db)
    team = await repo.get_by_id(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return TeamResponse.model_validate(team)


@router.get("/{team_id}/form")
async def get_team_form(team_id: int, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """Get team's recent form (last N matches)."""
    team_repo = TeamRepository(db)
    team = await team_repo.get_by_id(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    match_repo = MatchRepository(db)
    matches = await match_repo.get_team_matches(team_id, limit=limit)

    form = []
    for m in matches:
        if m.home_team_id == team_id:
            if m.home_score is not None and m.away_score is not None:
                if m.home_score > m.away_score:
                    form.append("W")
                elif m.home_score < m.away_score:
                    form.append("L")
                else:
                    form.append("D")
        else:
            if m.away_score is not None and m.home_score is not None:
                if m.away_score > m.home_score:
                    form.append("W")
                elif m.away_score < m.home_score:
                    form.append("L")
                else:
                    form.append("D")

    return {
        "team": TeamResponse.model_validate(team),
        "form": "".join(form),
        "matches": [
            {
                "id": m.id,
                "opponent": (m.away_team.name if m.home_team_id == team_id else m.home_team.name)
                if m.home_team and m.away_team else "?",
                "home_score": m.home_score,
                "away_score": m.away_score,
                "is_home": m.home_team_id == team_id,
                "date": m.match_date.isoformat(),
            }
            for m in matches
        ],
    }
