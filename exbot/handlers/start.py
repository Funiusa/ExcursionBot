from asyncio import sleep

from aiogram import types
import keyboards
import text
from dispatcher import dp
from keyboards.inline import inline_keyboard
from keyboards.keyboard import keyboards


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer(
        text=text.start.format(name=message.from_user.first_name),
        reply_markup=keyboards.main_keyboard,
    )
    await sleep(3)

    await message.answer(text=text.inline_start, reply_markup=inline_keyboard.menu)
