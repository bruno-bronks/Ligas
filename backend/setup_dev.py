import os
import shutil
import subprocess
import sys

def print_step(msg):
    print(f"\n==================================================")
    print(f"[STEP] {msg}")
    print(f"==================================================")

def main():
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(backend_dir)
    
    # 1. Copy root .env to backend/.env
    print_step("Copying root .env to backend/.env")
    root_env = os.path.join(root_dir, ".env")
    backend_env = os.path.join(backend_dir, ".env")
    
    if os.path.exists(root_env):
        shutil.copy2(root_env, backend_env)
        print("Successfully copied .env file.")
    else:
        print("Warning: Root .env file not found!")

    # 2. Setup virtual environment
    print_step("Setting up virtual environment in backend/.venv")
    venv_dir = os.path.join(backend_dir, ".venv")
    if not os.path.exists(venv_dir):
        subprocess.run([sys.executable, "-m", "venv", ".venv"], cwd=backend_dir, check=True)
        print("Virtual environment created.")
    else:
        print("Virtual environment already exists.")

    # 3. Determine python and pip executables
    if sys.platform == "win32":
        python_exe = os.path.join(venv_dir, "Scripts", "python.exe")
        pip_exe = os.path.join(venv_dir, "Scripts", "pip.exe")
    else:
        python_exe = os.path.join(venv_dir, "bin", "python")
        pip_exe = os.path.join(venv_dir, "bin", "pip")

    # 4. Install dependencies
    print_step("Installing dependencies")
    subprocess.run([python_exe, "-m", "pip", "install", "--upgrade", "pip"], cwd=backend_dir, check=True)
    subprocess.run([python_exe, "-m", "pip", "install", "-r", "requirements.txt", "aiosqlite"], cwd=backend_dir, check=True)
    print("Dependencies installed successfully.")

    # 5. Initialize alembic versions folder and generate migrations if not present
    print_step("Initializing migrations and generating schema")
    versions_dir = os.path.join(backend_dir, "alembic", "versions")
    if not os.path.exists(versions_dir):
        os.makedirs(versions_dir)
        print("Created alembic/versions directory.")
        
    # Generate the initial migration revision
    print("Generating Alembic migration revision...")
    subprocess.run([
        python_exe, "-m", "alembic", "revision", "--autogenerate", "-m", "initial_migration"
    ], cwd=backend_dir, check=True)
    
    # Run the migration
    print("Applying migration to database...")
    subprocess.run([
        python_exe, "-m", "alembic", "upgrade", "head"
    ], cwd=backend_dir, check=True)
    print("Database migrated successfully.")

    # 6. Seed leagues
    print_step("Seeding the leagues database")
    seed_script = """
import asyncio
from app.core.database import async_session_factory
from app.services.sync_service import SyncService

async def seed():
    print("Seeding leagues in database...")
    async with async_session_factory() as session:
        service = SyncService(session)
        result = await service.sync_leagues()
        await session.commit()
        print("Seeding completed successfully!")
        print("Results:", result)

if __name__ == '__main__':
    asyncio.run(seed())
"""
    temp_seed_path = os.path.join(backend_dir, "temp_seed.py")
    with open(temp_seed_path, "w", encoding="utf-8") as f:
        f.write(seed_script)
        
    try:
        subprocess.run([python_exe, "temp_seed.py"], cwd=backend_dir, check=True)
    finally:
        if os.path.exists(temp_seed_path):
            os.remove(temp_seed_path)
            
    print_step("Setup Completed Successfully!")

if __name__ == '__main__':
    main()
