import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    SECRET_KEY = os.getenv("APP_SECRET_KEY", "module5-development-secret")
    DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "tasks.db"))
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
