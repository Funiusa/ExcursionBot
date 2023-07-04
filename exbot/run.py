import logging

from aiogram import executor
from aiogram.dispatcher import Dispatcher

import config
from database.services import create_async_database
from utils.notify_admins import on_startup_notify
from utils.set_default_commands import set_default_commands
from handlers import dp


async def on_startup(dispatcher: Dispatcher):
    await create_async_database()
    await on_startup_notify(dispatcher)
    await set_default_commands(dispatcher)


def start_bot():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup,
        reset_webhook=True,
    )


if __name__ == "__main__":
    print("INFO DARAVASE", config.DATABASE_PASSWORD)
    start_bot()
