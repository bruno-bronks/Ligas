"""
Football Intelligence Dashboard - Sync Service
Orchestrates data fetching from API-Football and stores in database.
"""

from datetime import datetime
from typing import Optional

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import LEAGUES_CONFIG
from app.integrations.football_api import api_football_client
from app.models.league import League
from app.models.match import Match
from app.models.season import Season
from app.models.standing import Standing
from app.models.team import Team
from app.repositories.league_repository import LeagueRepository
from app.repositories.match_repository import MatchRepository
from app.repositories.standing_repository import StandingRepository
from app.repositories.team_repository import TeamRepository


class SyncService:
    """Orchestrates data synchronization from API-Football."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.league_repo = LeagueRepository(session)
        self.team_repo = TeamRepository(session)
        self.standing_repo = StandingRepository(session)
        self.match_repo = MatchRepository(session)

    async def sync_leagues(self) -> dict:
        """Seed/update all 14 leagues from config."""
        results = {"created": 0, "updated": 0, "errors": 0}

        for league_cfg in LEAGUES_CONFIG:
            try:
                existing = await self.league_repo.get_by_code(league_cfg["code"])
                if existing:
                    existing.name = league_cfg["name"]
                    existing.country = league_cfg["country"]
                    existing.flag_emoji = league_cfg.get("flag", "")
                    await self.league_repo.update(existing)
                    results["updated"] += 1
                else:
                    league = League(
                        name=league_cfg["name"],
                        country=league_cfg["country"],
                        code=league_cfg["code"],
                        api_football_id=league_cfg["api_football_id"],
                        flag_emoji=league_cfg.get("flag", ""),
                    )
                    await self.league_repo.create(league)
                    results["created"] += 1
            except Exception as e:
                logger.error(f"Error syncing league {league_cfg['code']}: {e}")
                results["errors"] += 1

        logger.info(f"Leagues sync: {results}")
        return results

    async def sync_teams(self, league_code: str, season: int) -> dict:
        """Sync teams for a league from API-Football."""
        results = {"created": 0, "updated": 0, "errors": 0}

        league = await self.league_repo.get_by_code(league_code)
        if not league:
            return {"error": f"League {league_code} not found"}

        api_teams = await api_football_client.get_teams(league.api_football_id, season)

        for team_data in api_teams:
            try:
                team_info = team_data.get("team", {})
                api_id = team_info.get("id")

                existing = await self.team_repo.get_by_api_football_id(api_id)
                if existing:
                    existing.name = team_info.get("name", existing.name)
                    existing.short_name = team_info.get("code", existing.short_name)
                    existing.logo_url = team_info.get("logo", existing.logo_url)
                    venue_info = team_data.get("venue", {})
                    if venue_info:
                        existing.venue = venue_info.get("name", existing.venue)
                    await self.team_repo.update(existing)
                    results["updated"] += 1
                else:
                    venue_info = team_data.get("venue", {})
                    team = Team(
                        name=team_info.get("name", "Unknown"),
                        short_name=team_info.get("code"),
                        code=team_info.get("code"),
                        api_football_id=api_id,
                        league_id=league.id,
                        logo_url=team_info.get("logo"),
                        venue=venue_info.get("name") if venue_info else None,
                        founded=team_info.get("founded"),
                    )
                    await self.team_repo.create(team)
                    results["created"] += 1
            except Exception as e:
                logger.error(f"Error syncing team: {e}")
                results["errors"] += 1

        logger.info(f"Teams sync for {league_code}: {results}")
        return results

    async def sync_standings(self, league_code: str, season_year: int) -> dict:
        """Sync standings for a league from API-Football."""
        results = {"upserted": 0, "errors": 0}

        league = await self.league_repo.get_by_code(league_code)
        if not league:
            return {"error": f"League {league_code} not found"}

        # Find or create season
        from sqlalchemy import select
        season_result = await self.session.execute(
            select(Season).where(
                Season.league_id == league.id,
                Season.year == str(season_year),
            )
        )
        season = season_result.scalar_one_or_none()
        if not season:
            season = Season(
                league_id=league.id,
                year=str(season_year),
                is_current=True,
            )
            self.session.add(season)
            await self.session.flush()

            # Deactivate other seasons for this league to maintain database integrity
            from sqlalchemy import update
            await self.session.execute(
                update(Season)
                .where(Season.league_id == league.id, Season.id != season.id)
                .values(is_current=False)
            )

        api_standings = await api_football_client.get_standings(
            league.api_football_id, season_year
        )

        for standing_data in api_standings:
            try:
                team_info = standing_data.get("team", {})
                api_team_id = team_info.get("id")
                team = await self.team_repo.get_by_api_football_id(api_team_id)
                if not team:
                    continue

                all_stats = standing_data.get("all", {})
                home_stats = standing_data.get("home", {})
                away_stats = standing_data.get("away", {})

                data = {
                    "position": standing_data.get("rank", 0),
                    "played": all_stats.get("played", 0),
                    "won": all_stats.get("win", 0),
                    "drawn": all_stats.get("draw", 0),
                    "lost": all_stats.get("lose", 0),
                    "goals_for": all_stats.get("goals", {}).get("for", 0),
                    "goals_against": all_stats.get("goals", {}).get("against", 0),
                    "goal_difference": standing_data.get("goalsDiff", 0),
                    "points": standing_data.get("points", 0),
                    "form": standing_data.get("form", ""),
                    "description": standing_data.get("description", ""),
                    "home_played": home_stats.get("played", 0),
                    "home_won": home_stats.get("win", 0),
                    "home_drawn": home_stats.get("draw", 0),
                    "home_lost": home_stats.get("lose", 0),
                    "home_goals_for": home_stats.get("goals", {}).get("for", 0),
                    "home_goals_against": home_stats.get("goals", {}).get("against", 0),
                    "away_played": away_stats.get("played", 0),
                    "away_won": away_stats.get("win", 0),
                    "away_drawn": away_stats.get("draw", 0),
                    "away_lost": away_stats.get("lose", 0),
                    "away_goals_for": away_stats.get("goals", {}).get("for", 0),
                    "away_goals_against": away_stats.get("goals", {}).get("against", 0),
                }

                await self.standing_repo.upsert(season.id, team.id, data)
                results["upserted"] += 1
            except Exception as e:
                logger.error(f"Error syncing standing: {e}")
                results["errors"] += 1

        logger.info(f"Standings sync for {league_code}: {results}")
        return results

    async def sync_fixtures(self, league_code: str, season_year: int) -> dict:
        """Sync fixtures/results for a league from API-Football."""
        results = {"created": 0, "updated": 0, "errors": 0}

        league = await self.league_repo.get_by_code(league_code)
        if not league:
            return {"error": f"League {league_code} not found"}

        from sqlalchemy import select
        season_result = await self.session.execute(
            select(Season).where(
                Season.league_id == league.id,
                Season.year == str(season_year),
            )
        )
        season = season_result.scalar_one_or_none()
        if not season:
            return {"error": f"Season {season_year} not found for {league_code}"}

        api_fixtures = await api_football_client.get_fixtures(
            league.api_football_id, season_year
        )

        for fixture_data in api_fixtures:
            try:
                fixture = fixture_data.get("fixture", {})
                teams = fixture_data.get("teams", {})
                goals = fixture_data.get("goals", {})
                score = fixture_data.get("score", {})

                api_fixture_id = fixture.get("id")

                home_api_id = teams.get("home", {}).get("id")
                away_api_id = teams.get("away", {}).get("id")

                home_team = await self.team_repo.get_by_api_football_id(home_api_id)
                away_team = await self.team_repo.get_by_api_football_id(away_api_id)

                if not home_team or not away_team:
                    continue

                # Detect G3 vs Z3
                standings = await self.standing_repo.get_by_season(season.id)
                is_g3_vs_z3 = False
                if len(standings) >= 6:
                    g3_ids = {s.team_id for s in standings[:3]}
                    z3_ids = {s.team_id for s in standings[-3:]}
                    is_g3_vs_z3 = (
                        (home_team.id in g3_ids and away_team.id in z3_ids)
                        or (home_team.id in z3_ids and away_team.id in g3_ids)
                    )

                match_date_str = fixture.get("date", "")
                try:
                    match_date = datetime.fromisoformat(match_date_str.replace("Z", "+00:00"))
                except (ValueError, AttributeError):
                    match_date = datetime.utcnow()

                ht = score.get("halftime", {})

                existing = await self.match_repo.get_by_api_football_id(api_fixture_id)
                if existing:
                    existing.status = fixture.get("status", {}).get("short", "NS")
                    existing.home_score = goals.get("home")
                    existing.away_score = goals.get("away")
                    existing.home_ht_score = ht.get("home")
                    existing.away_ht_score = ht.get("away")
                    existing.is_g3_vs_z3 = is_g3_vs_z3
                    existing.venue = fixture.get("venue", {}).get("name")
                    existing.referee = fixture.get("referee")
                    await self.match_repo.update(existing)
                    results["updated"] += 1
                else:
                    match = Match(
                        season_id=season.id,
                        home_team_id=home_team.id,
                        away_team_id=away_team.id,
                        api_football_id=api_fixture_id,
                        matchday=fixture_data.get("league", {}).get("round", "").split(" - ")[-1] if fixture_data.get("league", {}).get("round") else None,
                        match_date=match_date,
                        status=fixture.get("status", {}).get("short", "NS"),
                        home_score=goals.get("home"),
                        away_score=goals.get("away"),
                        home_ht_score=ht.get("home"),
                        away_ht_score=ht.get("away"),
                        venue=fixture.get("venue", {}).get("name"),
                        referee=fixture.get("referee"),
                        is_g3_vs_z3=is_g3_vs_z3,
                    )
                    # Parse matchday from round string
                    round_str = fixture_data.get("league", {}).get("round", "")
                    if "Regular Season" in round_str:
                        try:
                            match.matchday = int(round_str.split(" - ")[-1])
                        except (ValueError, IndexError):
                            pass

                    await self.match_repo.create(match)
                    results["created"] += 1
            except Exception as e:
                logger.error(f"Error syncing fixture: {e}")
                results["errors"] += 1

        logger.info(f"Fixtures sync for {league_code}: {results}")
        return results

    async def sync_all(self, season_year: int = 2024) -> dict:
        """Full sync: leagues → teams → standings → fixtures."""
        logger.info(f"Starting full sync for season {season_year}...")

        # 1. Sync leagues from config
        await self.sync_leagues()

        all_results = {}
        for league_cfg in LEAGUES_CONFIG:
            code = league_cfg["code"]
            logger.info(f"Syncing {code}...")

            # 2. Teams
            teams_result = await self.sync_teams(code, season_year)
            # 3. Standings
            standings_result = await self.sync_standings(code, season_year)
            # 4. Fixtures
            fixtures_result = await self.sync_fixtures(code, season_year)

            all_results[code] = {
                "teams": teams_result,
                "standings": standings_result,
                "fixtures": fixtures_result,
            }

        logger.info("Full sync completed!")
        return all_results
