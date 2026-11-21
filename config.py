
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # PostgreSQL configuration
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "licenseloop_db"
    DB_USER = "postgres"
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    # Flask authentication configuration
    SECRET_KEY = os.getenv("SECRET_KEY")

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = (
        os.getenv("SESSION_COOKIE_SECURE", "False").lower() == "true"
    )

    PERMANENT_SESSION_LIFETIME = 1800
