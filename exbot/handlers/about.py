from aiogram import types
from dispatcher import dp
from content.about import about


@dp.message_handler(commands=["about"])
async def about_handler(message: types.message):
    await message.answer(about)
