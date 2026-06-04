print("Testing imports...")
import os
print("Importing config...")
from app.core.config import get_settings
settings = get_settings()
print("Settings loaded:", settings.DATABASE_URL)

print("Importing database...")
from app.core.database import Base

print("Importing models...")
from app.models import *
print("Models imported successfully!")

print("Importing alembic env code...")
from alembic.config import Config
from alembic import command
print("Alembic imported successfully!")
