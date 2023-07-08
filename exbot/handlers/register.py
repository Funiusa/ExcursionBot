from aiogram import filters, types
from aiogram.dispatcher import FSMContext

from database import crud, schemas
from database.base import db
from dispatcher import dp
from keyboards.inline import ikb
from keyboards.keyboard.keyboards import main_keyboard
from state.register import Registration
from utils.tools import phone_validation


@dp.message_handler(commands=["registration"])
async def registration_handler(message: types.Message):
    ikb.register_ikb.inline_keyboard.clear()
    ikb.register_ikb.add(*ikb.ikb)
    await message.answer(
        "Please send me your contact for registration", reply_markup=ikb.register_ikb
    )


@dp.callback_query_handler(filters.Text("remove_ikb"))
async def cancel_registration(call: types.CallbackQuery):
    await call.answer()
    await call.message.delete()


@dp.callback_query_handler(filters.Text("registration_state"))
async def registration_state_handler(call: types.CallbackQuery):
    await call.answer()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb = types.KeyboardButton("Send my contact", request_contact=True)
    markup.add(kb)
    telegram_id = call.from_user.id

    user = await crud.users.get_user_by_telegram_id(telegram_id=telegram_id, db=db)
    if not user:
        await call.message.delete()
        await Registration.contact.set()
        await call.message.answer(
            text="Push the button below to send your contact", reply_markup=markup
        )
    else:
        await call.message.answer(text="You already registered")


@dp.message_handler(content_types=types.ContentType.CONTACT, state=Registration.contact)
async def contact_handler(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    telegram_id = message.contact.user_id
    username = message.chat.username

    await state.update_data(phone=phone, telegram_id=telegram_id, username=username)
    await check_contact(message=message, state=state)


async def check_contact(message: types.message, state: FSMContext):
    data = await state.get_data()
    telegram_id = data["telegram_id"]
    username = data["username"]
    phone = data["phone"]
    if phone_validation(phone):
        data = {"telegram_id": telegram_id, "username": username, "phone": phone}
        user_data = schemas.UserCreate(**data)
        await crud.users.create_user(user=user_data, db=db)
        await message.delete()
        await state.finish()
        text = "Your contact was successfully registered"
        await message.answer(text=text, reply_markup=main_keyboard)
    else:
        await message.answer("Your phon number is not valid")


@dp.callback_query_handler(filters.Text("registration_block"))
async def show_start(call: types.CallbackQuery):
    await call.answer()
    ikb.register_ikb.inline_keyboard.clear()

    ikb.register_ikb.add(*ikb.ikb)
    await call.message.edit_text(
        "Please send me your contact for registration", reply_markup=ikb.register_ikb
    )
