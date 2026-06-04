"""
Match API endpoints.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.match_repository import MatchRepository
from app.schemas.match import G3vsZ3Response

router = APIRouter()


@router.get("")
async def list_matches(
    status: Optional[str] = None,
    page: int = 1,
    per_page: int = 20,
    db: AsyncSession = Depends(get_db),
):
    """List matches with optional filters."""
    repo = MatchRepository(db)

    if status == "live":
        matches = await repo.get_live_matches()
    else:
        matches = await repo.get_all(skip=(page - 1) * per_page, limit=per_page)

    return {
        "matches": [
            {
                "id": m.id,
                "home_team": m.home_team.name if m.home_team else "?",
                "away_team": m.away_team.name if m.away_team else "?",
                "home_team_logo": m.home_team.logo_url if m.home_team else None,
                "away_team_logo": m.away_team.logo_url if m.away_team else None,
                "home_score": m.home_score,
                "away_score": m.away_score,
                "status": m.status,
                "match_date": m.match_date.isoformat(),
                "is_g3_vs_z3": m.is_g3_vs_z3,
            }
            for m in matches
        ],
        "total": len(matches),
        "page": page,
        "per_page": per_page,
    }


@router.get("/g3-vs-z3")
async def get_g3_vs_z3_matches(db: AsyncSession = Depends(get_db)):
    """Get all G3 vs Z3 highlighted matches."""
    repo = MatchRepository(db)
    all_g3z3 = await repo.get_g3_vs_z3()

    upcoming = [m for m in all_g3z3 if m.status == "NS"]
    recent = [m for m in all_g3z3 if m.status == "FT"]

    def serialize(m):
        return {
            "id": m.id,
            "home_team": m.home_team.name if m.home_team else "?",
            "away_team": m.away_team.name if m.away_team else "?",
            "home_team_logo": m.home_team.logo_url if m.home_team else None,
            "away_team_logo": m.away_team.logo_url if m.away_team else None,
            "home_score": m.home_score,
            "away_score": m.away_score,
            "status": m.status,
            "match_date": m.match_date.isoformat(),
            "is_g3_vs_z3": True,
        }

    return {
        "upcoming": [serialize(m) for m in upcoming[:20]],
        "recent": [serialize(m) for m in recent[:20]],
        "total": len(all_g3z3),
    }


@router.get("/{match_id}")
async def get_match_detail(match_id: int, db: AsyncSession = Depends(get_db)):
    """Get full match details with prediction and analysis."""
    repo = MatchRepository(db)
    match = await repo.get_match_detail(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    result = {
        "id": match.id,
        "home_team": match.home_team.name if match.home_team else "?",
        "away_team": match.away_team.name if match.away_team else "?",
        "home_team_logo": match.home_team.logo_url if match.home_team else None,
        "away_team_logo": match.away_team.logo_url if match.away_team else None,
        "home_score": match.home_score,
        "away_score": match.away_score,
        "home_ht_score": match.home_ht_score,
        "away_ht_score": match.away_ht_score,
        "home_xg": match.home_xg,
        "away_xg": match.away_xg,
        "status": match.status,
        "match_date": match.match_date.isoformat(),
        "matchday": match.matchday,
        "venue": match.venue,
        "referee": match.referee,
        "is_g3_vs_z3": match.is_g3_vs_z3,
    }

    # Prediction
    if match.prediction:
        result["prediction"] = {
            "home_win_prob": match.prediction.home_win_prob,
            "draw_prob": match.prediction.draw_prob,
            "away_win_prob": match.prediction.away_win_prob,
            "over_2_5_prob": match.prediction.over_2_5_prob,
            "btts_prob": match.prediction.btts_prob,
            "predicted_outcome": match.prediction.predicted_outcome,
        }

    # AI Analysis
    if match.ai_analysis:
        result["ai_analysis"] = {
            "text": match.ai_analysis.analysis_text,
            "provider": match.ai_analysis.llm_provider,
            "model": match.ai_analysis.model_name,
        }

    return result


@router.post("/{match_id}/analyze")
async def analyze_match(match_id: int, db: AsyncSession = Depends(get_db)):
    """Generate and save AI analysis for a match."""
    from app.repositories.match_repository import MatchRepository
    from app.models.ai_analysis import AIAnalysis
    from app.integrations.llm_client import get_llm_provider
    from sqlalchemy import select
    from app.models.standing import Standing

    repo = MatchRepository(db)
    match = await repo.get_match_detail(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    # If already analyzed, return it
    if match.ai_analysis:
        return {
            "text": match.ai_analysis.analysis_text,
            "provider": match.ai_analysis.llm_provider,
            "model": match.ai_analysis.model_name,
        }

    # Fetch standings for context
    home_standing = (await db.execute(
        select(Standing).where(Standing.season_id == match.season_id, Standing.team_id == match.home_team_id)
    )).scalar_one_or_none()

    away_standing = (await db.execute(
        select(Standing).where(Standing.season_id == match.season_id, Standing.team_id == match.away_team_id)
    )).scalar_one_or_none()

    # Build prompt
    home_name = match.home_team.name if match.home_team else "Home Team"
    away_name = match.away_team.name if match.away_team else "Away Team"
    league_name = match.season.league.name if match.season and match.season.league else "League"
    
    prompt = f"""
    You are an expert football tactical analyst. Analyze this upcoming match:
    Match: {home_name} vs {away_name}
    League: {league_name}
    Date: {match.match_date}
    
    Home Team Standing:
    - Position: {home_standing.position if home_standing else 'N/A'}
    - Points: {home_standing.points if home_standing else 'N/A'}
    - Form: {home_standing.form if home_standing else 'N/A'}
    - Played/Won/Drawn/Lost: {home_standing.played if home_standing else 'N/A'}/{home_standing.won if home_standing else 'N/A'}/{home_standing.drawn if home_standing else 'N/A'}/{home_standing.lost if home_standing else 'N/A'}
    - Goal Diff: {home_standing.goal_difference if home_standing else 'N/A'}
    
    Away Team Standing:
    - Position: {away_standing.position if away_standing else 'N/A'}
    - Points: {away_standing.points if away_standing else 'N/A'}
    - Form: {away_standing.form if away_standing else 'N/A'}
    - Played/Won/Drawn/Lost: {away_standing.played if away_standing else 'N/A'}/{away_standing.won if away_standing else 'N/A'}/{away_standing.drawn if away_standing else 'N/A'}/{away_standing.lost if away_standing else 'N/A'}
    - Goal Diff: {away_standing.goal_difference if away_standing else 'N/A'}
    
    Provide your analysis in Markdown, structured into three sections:
    1. ### 🏟️ Tactical Preview & Analysis
    2. ### 🔑 Key Factors & Matchups
    3. ### 🎯 Predicted Outcome & Rationale
    """

    system_prompt = "You are a professional football analyst producing detailed tactical preview summaries."

    llm = get_llm_provider()
    analysis_text = await llm.generate(prompt, system_prompt)

    # Save to database
    ai_analysis = AIAnalysis(
        match_id=match.id,
        analysis_text=analysis_text,
        llm_provider=llm.__class__.__name__,
        model_name=llm.get_model_name(),
    )
    db.add(ai_analysis)
    await db.commit()

    return {
        "text": analysis_text,
        "provider": ai_analysis.llm_provider,
        "model": ai_analysis.model_name,
    }

