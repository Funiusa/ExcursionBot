import logging

from aiogram import Dispatcher
from sqlalchemy import select

from database import base, models


async def on_startup_notify(dp: Dispatcher):
    async with base.AsyncSessionLocal() as session:
        stmt = select(models.Admin).filter_by(is_superuser=True)
        result = await session.execute(statement=stmt)
        admins = result.scalars().all()

        for admin in admins:
            try:
                print("\n\n\nBOT START\n")
                text = "Bot launched successfully"
                await dp.bot.send_message(chat_id=admin.telegram_id, text=text)
            except Exception as e:
                logging.exception(e)
