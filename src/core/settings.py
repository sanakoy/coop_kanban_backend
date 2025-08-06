from dotenv import load_dotenv
import os


load_dotenv()

class Settings:
    # Получение данных из .env
    db_config = {
        "driver": os.getenv("DB_DRIVER", "postgresql+asyncpg"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "name": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    }

    # Формирование DSN
    database_url = (
        f"{db_config['driver']}://"
        f"{db_config['user']}:{db_config['password']}@"
        f"{db_config['host']}:{db_config['port']}/"
        f"{db_config['name']}"
    )

settings = Settings()