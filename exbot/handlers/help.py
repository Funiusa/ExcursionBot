from aiogram import types
import keyboards
import text
from dispatcher import dp


@dp.message_handler(regexp="список команд")
@dp.message_handler(commands=["help"])
async def help_handler(message: types.message):
    await message.answer(text.help)
