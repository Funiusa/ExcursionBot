from aiogram import types, filters
from dispatcher import dp
from content.main_text import commands_list
from keyboards.inline.ikb import main_menu


@dp.message_handler(text="Список команд")
@dp.message_handler(commands=["commands"])
async def commands_list_handler(message: types.message):
    await message.answer(text=commands_list)


@dp.callback_query_handler(filters.Text("commands_list"))
async def show_commands_list(call: types.CallbackQuery):
    await call.answer()

    await call.message.edit_text(text=commands_list, reply_markup=main_menu)
