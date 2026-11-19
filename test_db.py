
import psycopg
from config import Config

try:
    connection = psycopg.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD
    )

    print("PostgreSQL connection successful!")

    cursor = connection.cursor()
    cursor.execute("SELECT current_database();")

    database_name = cursor.fetchone()[0]

    print("Connected database:", database_name)

    cursor.close()
    connection.close()

except Exception as error:
    print("Database connection failed!")
    print(error)
