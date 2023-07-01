from aiogram import types, filters
import text
from dispatcher import dp
from keyboards.inline.ikb import main_menu
from keyboards.keyboard.keyboards import main_keyboard


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer(
        text=text.start.format(name=message.from_user.first_name),
        reply_markup=main_menu,
    )


@dp.callback_query_handler(filters.Text("start_block"))
async def show_start(call: types.CallbackQuery):
    await call.answer()
    start_text = text.start.format(name=call.message.from_user.first_name)
    await call.message.edit_text(text=start_text, reply_markup=main_menu)
