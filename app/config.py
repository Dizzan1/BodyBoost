from pathlib import Path
import os
import secrets
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))
DB_PATH = os.getenv("DB_PATH", str(BASE_DIR / "db" / "bodyboost.db"))
DATA_PATH = os.getenv("DATA_PATH", str(BASE_DIR / "app" / "data" / "exercises.json"))