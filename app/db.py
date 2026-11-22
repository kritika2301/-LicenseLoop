
import psycopg
from config import Config


def get_db_connection():

    # Use hosted database URL when available
    if Config.DATABASE_URL:

        connection = psycopg.connect(
            Config.DATABASE_URL,
            sslmode="require"
        )

    else:

        # Use local PostgreSQL configuration
        connection = psycopg.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )

    return connection
