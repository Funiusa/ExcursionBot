from aiogram import filters, types

from content import help
from dispatcher import dp
from keyboards.inline.ikb import back_to_main_menu

help_menu = types.InlineKeyboardMarkup(row_width=1)
ikb = [
    types.InlineKeyboardButton(text=block["title"], callback_data=f"help_title_{index}")
    for index, block in enumerate(help.help_text)
]


@dp.message_handler(commands=["help"])
async def help_handler(message: types.Message):
    help_menu.inline_keyboard.clear()
    help_menu.add(*ikb)
    await message.answer(text=help.about, reply_markup=help_menu)


@dp.callback_query_handler(
    lambda c: c.data.startswith("help_title_") or c.data.startswith("help_back_")
)
async def callback_inline(call: types.CallbackQuery):
    if call.data == "help_back_":
        await call.message.edit_text(text=help.about, reply_markup=help_menu)
    else:
        index = int(call.data.split("_")[-1])
        text = help.help_text[index]["text"]
        await call.message.edit_text(text=text, reply_markup=help_menu)


@dp.callback_query_handler(filters.Text("help_block"))
async def open_help(call: types.CallbackQuery):
    await call.answer()

    help_menu.inline_keyboard.clear()
    help_menu.add(*ikb, back_to_main_menu)
    await call.message.edit_text(text=help.about, reply_markup=help_menu)
