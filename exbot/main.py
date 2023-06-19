import asyncio
import logging
from dispatcher import bot
from handlers import dp
from config import POSTGRES_URL
from db import BaseModel, create_engine, proceed_schemas, get_session_maker


async def on_startup():
    from utils.notify_admins import on_startup_notify

    await bot.delete_webhook(drop_pending_updates=True)
    await on_startup_notify(dp)
    logging.info("Bot launched successfully")

    from utils.set_bot_commands import set_default_commands

    await set_default_commands(dp)
    async_engine = create_engine(POSTGRES_URL)
    session_maker = get_session_maker(async_engine)
    await proceed_schemas(async_engine, BaseModel.metadata)


async def main():
    await on_startup()
    await dp.start_polling()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(dp.storage.close())
        loop.run_until_complete(dp.storage.wait_closed())
        loop.close()
