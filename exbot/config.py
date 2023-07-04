import os
from sqlalchemy import URL
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]
# PAY_TOKEN = os.environ["PAY_TOKEN"]
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("POSTGRES_USER")
DATABASE_PASSWORD = os.getenv("POSTGRES_USER")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")

admins_id = os.getenv("ADMINS")

url = URL.create(
    "postgresql+asyncpg",
    username=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=int(DATABASE_PORT),
    database=DATABASE_NAME,
)
