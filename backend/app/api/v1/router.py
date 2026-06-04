"""
Football Intelligence Dashboard - API v1 Router
Central router aggregating all v1 endpoints.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import leagues, matches, teams, dashboard, auth, admin

api_router = APIRouter()

api_router.include_router(leagues.router, prefix="/leagues", tags=["Leagues"])
api_router.include_router(teams.router, prefix="/teams", tags=["Teams"])
api_router.include_router(matches.router, prefix="/matches", tags=["Matches"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
