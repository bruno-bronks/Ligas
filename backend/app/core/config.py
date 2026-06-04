"""
Football Intelligence Dashboard - Core Configuration
Centralized settings management using Pydantic Settings.
"""

from functools import lru_cache
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- App ---
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    FRONTEND_URL: str = "http://localhost:3000"
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    # --- Database ---
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/football_intelligence"
    DATABASE_URL_SYNC: str = "postgresql://postgres:postgres@localhost:5432/football_intelligence"

    # --- Redis ---
    REDIS_URL: str = "redis://localhost:6379/0"

    # --- API-Football ---
    API_FOOTBALL_KEY: str = ""
    API_FOOTBALL_BASE_URL: str = "https://v3.football.api-sports.io"

    # --- LLM ---
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    LLM_PROVIDER: str = "gemini"  # "openai" or "gemini"

    # --- WhatsApp ---
    WHATSAPP_NUMBERS: str = ""
    WHATSAPP_API_KEYS: str = ""
    CALLMEBOT_URL: str = "https://api.callmebot.com/whatsapp.php"

    @property
    def whatsapp_recipients(self) -> List[dict]:
        numbers = [n.strip() for n in self.WHATSAPP_NUMBERS.split(",") if n.strip()]
        keys = [k.strip() for k in self.WHATSAPP_API_KEYS.split(",") if k.strip()]
        return [{"phone": n, "apikey": k} for n, k in zip(numbers, keys)]

    # --- Telegram ---
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_CHAT_IDS: str = ""

    @property
    def telegram_chat_ids_list(self) -> List[str]:
        return [cid.strip() for cid in self.TELEGRAM_CHAT_IDS.split(",") if cid.strip()]

    # --- Email ---
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: Optional[str] = None

    # --- JWT ---
    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 1440


# League Configuration - All 14 leagues with API-Football IDs
LEAGUES_CONFIG = [
    {
        "name": "Premier League",
        "country": "England",
        "code": "PL",
        "api_football_id": 39,
        "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    },
    {
        "name": "Bundesliga",
        "country": "Germany",
        "code": "BL1",
        "api_football_id": 78,
        "flag": "🇩🇪",
    },
    {
        "name": "Premier League",
        "country": "Russia",
        "code": "RPL",
        "api_football_id": 235,
        "flag": "🇷🇺",
    },
    {
        "name": "La Liga",
        "country": "Spain",
        "code": "PD",
        "api_football_id": 140,
        "flag": "🇪🇸",
    },
    {
        "name": "Eredivisie",
        "country": "Netherlands",
        "code": "DED",
        "api_football_id": 88,
        "flag": "🇳🇱",
    },
    {
        "name": "Primeira Liga",
        "country": "Portugal",
        "code": "PPL",
        "api_football_id": 94,
        "flag": "🇵🇹",
    },
    {
        "name": "Serie A",
        "country": "Italy",
        "code": "SA",
        "api_football_id": 135,
        "flag": "🇮🇹",
    },
    {
        "name": "Ligue 1",
        "country": "France",
        "code": "FL1",
        "api_football_id": 61,
        "flag": "🇫🇷",
    },
    {
        "name": "Süper Lig",
        "country": "Turkey",
        "code": "TSL",
        "api_football_id": 203,
        "flag": "🇹🇷",
    },
    {
        "name": "Super League 1",
        "country": "Greece",
        "code": "GSL",
        "api_football_id": 197,
        "flag": "🇬🇷",
    },
    {
        "name": "Pro League",
        "country": "Saudi Arabia",
        "code": "SAL",
        "api_football_id": 307,
        "flag": "🇸🇦",
    },
    {
        "name": "Stars League",
        "country": "Qatar",
        "code": "QSL",
        "api_football_id": 305,
        "flag": "🇶🇦",
    },
    {
        "name": "Liga MX",
        "country": "Mexico",
        "code": "MXL",
        "api_football_id": 262,
        "flag": "🇲🇽",
    },
    {
        "name": "Premiership",
        "country": "Scotland",
        "code": "SPL",
        "api_football_id": 179,
        "flag": "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    },
]


@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()
