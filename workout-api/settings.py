"""
This module contains the settings for the application.
from .env file
"""
from dotenv import dotenv_values

config = dotenv_values(".env") or dotenv_values("../.env")
APP_PORT = 8000
app_url = f"http://localhost:{APP_PORT}"

HOST = 'localhost'
database = config.get("DATABASE")
user = config.get("DB_USER")
password = config.get("DB_PASSWORD")

test_database = config.get("TEST_DATABASE") or 'test_workout_db'
test_user = config.get("TEST_DB_USER") or 'test_user'
test_password = config.get("TEST_DB_PASSWORD") or 'test_password'

connection_string = f"postgresql+asyncpg://{user}:{password}@{HOST}/{database}"
test_connection_string = f"postgresql+asyncpg://{test_user}:{test_password}@{HOST}:5433/{test_database}"

SECRET_KEY = config.get("SECRET_KEY")
