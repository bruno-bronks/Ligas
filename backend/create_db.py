import asyncio
from app.core.database import Base, engine
# Import all models to ensure they are registered with the Base metadata
from app.models.league import League
from app.models.season import Season
from app.models.team import Team
from app.models.standing import Standing
from app.models.match import Match
from app.models.head_to_head import HeadToHead
from app.models.prediction import Prediction
from app.models.ai_analysis import AIAnalysis
from app.models.notification_log import NotificationLog
from app.models.user import User

async def create_tables():
    print("Creating tables in database via SQLAlchemy...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("All tables created successfully!")

if __name__ == '__main__':
    asyncio.run(create_tables())
