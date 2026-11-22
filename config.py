
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:

    # PostgreSQL configuration
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "licenseloop_db")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    # Optional hosted PostgreSQL connection URL
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Flask security configuration
    SECRET_KEY = os.getenv("SECRET_KEY")

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    SESSION_COOKIE_SECURE = (
        os.getenv("SESSION_COOKIE_SECURE", "False").lower()
        == "true"
    )

    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
