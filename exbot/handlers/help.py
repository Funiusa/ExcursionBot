from asyncio import sleep

from aiogram import types
from content import help
from dispatcher import dp, bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton


async def block_handler(message: types.Message, text: str, block_index: int):
    if block_index < len(help.help):
        block = help.help[block_index]
        title = block["title"]
        button = InlineKeyboardButton(text=title, callback_data=f"block_{block_index}")
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(button)
        await message.answer(text, reply_markup=keyboard)
    else:
        await message.answer(text)
    await message.delete_reply_markup()


@dp.message_handler(commands=["help"])
async def help_handler(message: types.Message):
    block = help.help[0]
    text = block["text"]
    await block_handler(message, text, 1)


@dp.callback_query_handler(lambda c: c.data.startswith("block_"))
async def callback_handler(callback_query: types.CallbackQuery):
    block_index = int(callback_query.data.split("_")[1])
    block = help.help[block_index]
    text = block["text"]
    await bot.answer_callback_query(callback_query.id)
    await block_handler(callback_query.message, text, block_index + 1)
