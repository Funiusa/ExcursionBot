from asyncio import sleep

from aiogram import types
import keyboards
import text
from dispatcher import dp
from keyboards.inline.menu import inline_menu


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
    inline_keyboard.add(*keyboards.inline_main_menu)
    replay_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    replay_keyboard.add(*keyboards.main_buttons)

    await message.answer(
        text=text.start.format(name=message.from_user.first_name),
        reply_markup=replay_keyboard,
    )
    await sleep(3)

    await message.answer(text=text.inline_start, reply_markup=inline_menu)
