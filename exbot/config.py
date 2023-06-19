import os

from sqlalchemy import URL

BOT_TOKEN = os.environ.get("BOT_TOKEN")
USERNAME = os.environ.get("POSTGRES_USER")
PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_NAME = os.environ.get("DATABASE_NAME")
HOST = os.environ.get("DATABASE_HOST")
PORT = os.environ.get("DATABASE_PORT")

POSTGRES_URL = URL.create(
    "postgresql+asyncpg",
    username=USERNAME,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    database=DB_NAME,
)

admins_id = [
    292612693,
]
