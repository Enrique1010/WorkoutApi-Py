from dotenv import dotenv_values

config = dotenv_values(".env") or dotenv_values("../.env")
APP_PORT = 8000
app_url = f"http://localhost:{APP_PORT}"

HOST = 'localhost'
database = config.get("DATABASE")
user = config.get("DB_USER")
password = config.get("DB_PASSWORD")

connection_string = f"postgresql+asyncpg://{user}:{password}@{HOST}/{database}"

SECRET_KEY = config.get("SECRET_KEY")
