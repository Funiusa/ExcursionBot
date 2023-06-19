import logging
from aiogram import Dispatcher

import keyboards
from config import admins_id


async def on_startup_notify(dp: Dispatcher):
    for admin in admins_id:
        try:
            text = "Bot launched successfully"
            await dp.bot.send_message(
                chat_id=admin, text=text, reply_markup=keyboards.main_keyboard
            )
        except Exception as e:
            logging.exception(e)
