from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
import text
from dispatcher import dp
from state import Registration


@dp.message_handler(commands=["registration"])
async def registration_handler(message: types.Message):
    await message.answer("Регистрация\n\nВведите имя:")
    await Registration.state1.set()


@dp.message_handler(state=Registration.state1)
async def state1(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(state1=answer)
    await message.answer(f"{answer}, сколько вам лет?")
    await Registration.state2.set()


@dp.message_handler(state=Registration.state2)
async def state2(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(state2=answer)
    data = await state.get_data()
    name, age = data.get("state1"), data.get("state2")
    await message.answer(f"{name.capitalize()}, регистрация успешно завершена.\nТебе {age} лет")
    await state.finish()
