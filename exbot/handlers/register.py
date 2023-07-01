from aiogram import types, filters
from aiogram.dispatcher import FSMContext
from sqlalchemy import select

from database import services, schemas
from database.base import session
from dispatcher import dp
from state.register import Registration
from database.models import User
from utils.tools import phone_validation
from keyboards.keyboard.keyboards import main_keyboard
from keyboards.inline import ikb


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

    result = session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.one_or_none()
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
    user = await services.get_user_by_telegram_id(telegram_id=telegram_id, db=session)
    if not user and phone_validation(phone):
        data = {"telegram_id": telegram_id, "username": username, "phone": phone}
        user_create = schemas.UserCreate(**data)
        await services.create_user(user_create, session)
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
