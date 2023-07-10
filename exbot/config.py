import os

from dotenv import load_dotenv
from sqlalchemy import URL

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]
# PAY_TOKEN = os.environ["PAY_TOKEN"]
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("POSTGRES_USER")
DATABASE_PASSWORD = os.getenv("POSTGRES_USER")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")

SU_USER_TELEGRAM = int(os.environ["SU_USER_TELEGRAM"])
SU_USERNAME = os.environ["SU_USERNAME"]
SU_USER_EMAIL = os.environ["SU_USER_EMAIL"]
SU_USER_PASS = os.environ["SU_USER_PASS"]

url = URL.create(
    "postgresql+asyncpg",
    username=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=int(DATABASE_PORT),
    database=DATABASE_NAME,
)

alembic_url = f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(BASE_DIR, "static")
STATIC_IMG = os.path.join(STATIC, "images")
