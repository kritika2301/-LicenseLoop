import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "licenseloop_db"
    DB_USER = "postgres"
    DB_PASSWORD = os.getenv("DB_PASSWORD")