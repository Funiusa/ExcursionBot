import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
USERNAME = os.environ.get("POSTGRES_USER")
PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_NAME = os.environ.get("DATABASE_NAME")
HOST = os.environ.get("DATABASE_HOST")
PORT = os.environ.get("DATABASE_PORT")

POSTGRES_URI = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

admins_id = [
    292612693,
]
