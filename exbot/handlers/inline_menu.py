from asyncio import sleep

from aiogram import types

from dispatcher import dp
from keyboards.inline import ikb


@dp.message_handler(text="menu")
async def show_inline_menu(message: types.Message):
    await message.answer("Inline menu", reply_markup=inline_keyboard.menu)


@dp.callback_query_handler(text="alert")
async def send_message(call: types.CallbackQuery):
    await call.answer("Вам необходимо зарегистрирваться.")


@dp.callback_query_handler(text="OK")
async def send_message(call: types.CallbackQuery):
    await call.answer(text="Все ОК?", show_alert=True)
    sticker_path = "data/sticker.webp"
    with open(sticker_path, "rb") as sticker:
        await sleep(2)
        await call.message.answer_sticker(sticker)
