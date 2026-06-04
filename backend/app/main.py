"""
Football Intelligence Dashboard - FastAPI Application Factory
"""

import socket
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

# Patch socket.getaddrinfo to resolve media.api-sports.io to its Cloudflare IP address.
# This works around local DNS resolution failures.
original_getaddrinfo = socket.getaddrinfo

def patched_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    if isinstance(host, bytes):
        host_str = host.decode("utf-8", errors="ignore")
    else:
        host_str = host

    if host_str == "media.api-sports.io" or (host_str and host_str.endswith("api-sports.io") and host_str.startswith("media-")):
        # Resolve using Cloudflare CDN IP (which is also used by v3.football.api-sports.io)
        return original_getaddrinfo("172.66.164.245", port, family, type, proto, flags)
    return original_getaddrinfo(host, port, family, type, proto, flags)

socket.getaddrinfo = patched_getaddrinfo

from app.core.config import get_settings, LEAGUES_CONFIG

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management."""
    logger.info("🏟️  Football Intelligence Dashboard starting up...")
    logger.info(f"📡 Environment: {settings.APP_ENV}")
    logger.info(f"⚽ Tracking {len(LEAGUES_CONFIG)} leagues")

    # Initialize Redis connection
    from app.core.dependencies import get_redis
    redis = await get_redis()
    logger.info("🔴 Redis connected")

    yield

    # Cleanup
    if redis:
        await redis.close()
    logger.info("🏟️  Football Intelligence Dashboard shutting down...")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Football Intelligence Dashboard API",
        description="Advanced football analytics, predictions, and intelligent notifications across 14 leagues.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    from app.api.v1.router import api_router
    app.include_router(api_router, prefix="/api/v1")

    @app.get("/health", tags=["Health"])
    async def health_check():
        return {
            "status": "healthy",
            "service": "Football Intelligence Dashboard",
            "version": "1.0.0",
            "leagues_tracked": len(LEAGUES_CONFIG),
        }

    return app


app = create_app()
