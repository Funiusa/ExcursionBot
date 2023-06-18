from aiogram import types
from dispatcher import dp
from content.main_text import commands_list


@dp.message_handler(text="Список команд")
@dp.message_handler(commands=["commands"])
async def about_handler(message: types.message):
    await message.answer(commands_list)
