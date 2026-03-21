import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_ROTATION_SIZE = 10 * 1024 * 1024
LOG_BACKUP_COUNT = 5

DATABASE_URL = "sqlite+aiosqlite:///./travel_app.db"

HOST = "127.0.0.1"
PORT = 8000
RELOAD = True
