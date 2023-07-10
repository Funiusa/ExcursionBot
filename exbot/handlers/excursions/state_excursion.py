from aiogram import types
from aiogram.dispatcher import FSMContext

from database import crud, base
from dispatcher import bot, dp
from keyboards.keyboard import keyboards
from state import QuestionsState
from utils.tools import clear_answer, get_addition_data

excursion_ikb = types.InlineKeyboardMarkup()


@dp.callback_query_handler(lambda c: c.data.startswith("guide_"))
async def guide_introduction_handler(call: types.CallbackQuery):
    await call.answer()
    data = call.data.split("_")
    guide_title = data[1]
    # guide = next((g for g in guides if g["title"] == guide_title), None)

    guide = await crud.excursions.get_excursion_by_title(title=guide_title, db=base.db)
    message_id = call.message.message_id
    back_button = types.InlineKeyboardButton(
        "Назад", callback_data=f"guides_end_{guide_title}_{message_id}"
    )
    start_button = types.InlineKeyboardButton(
        "Задание", callback_data=f"question_state_{guide_title}"
    )
    excursion_ikb.inline_keyboard.clear()
    excursion_ikb.add(back_button, start_button)
    image_path = guide.image
    intro = guide.description
    if image_path:
        with open(image_path, "rb") as photo:
            await bot.send_photo(
                chat_id=call.message.chat.id,
                photo=photo,
                caption=intro,  # max length 1024
                reply_markup=excursion_ikb,
            )
    else:
        await call.message.edit_text(text=intro, reply_markup=excursion_ikb)


@dp.callback_query_handler(lambda c: c.data.startswith("question_state_"))
async def start_handler(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data.split("_")
    guide_title = data[-1]
    guide = await crud.excursions.get_excursion_by_title(title=guide_title, db=base.db)
    questions = [q for q in guide.questions]
    await state.update_data(questions=questions)
    await ask_next_question(message=callback_query.message, state=state, index=0)


async def ask_next_question(message: types.Message, state: FSMContext, index: int):
    data = await state.get_data()
    try:
        question = data["questions"][index]
        place_image = question.place
        if place_image:
            with open(place_image, "rb") as photo:
                await bot.send_photo(
                    chat_id=message.chat.id,
                    reply_markup=keyboards.on_place,
                    photo=photo,
                )
            await state.update_data(
                index=index,
                hint=question.hint,
                answer=question.answer,
                correct=question.correct,
                text=question.text,
                addition=get_addition_data(path=question.addition),
                final=question.final,
            )
            await QuestionsState.question.set()
    except IndexError:
        await message.answer("Вы прошли ознокомительный блок")
        path = "data/end.jpg"
        with open(path, "rb") as photo:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                reply_markup=keyboards.main_keyboard,
            )
        await state.finish()


@dp.message_handler(text="На месте", state=QuestionsState.question)
async def get_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    path = data["text"]
    with open(path, "rb") as image:
        await message.answer_photo(photo=image, reply_markup=keyboards.complete)
    await state.update_data(hint=None)
    await message.answer("Вводи ответ и жми отправить! 👇🏽")


@dp.message_handler(state=QuestionsState.question)
async def answer_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    correct_answer = data["answer"]
    hint = data["hint"]
    index = data["index"]
    correct = data["correct"]
    final = data["final"]
    addition = data["addition"]
    answer = clear_answer(str(message.text))
    inline_next = types.InlineKeyboardMarkup()

    next_question = types.InlineKeyboardButton(
        "Следующий этап", callback_data=f"next_question_{index}"
    )
    inline_next.add(next_question)

    if answer == correct_answer:
        await message.answer(text="Ответ правильный!:)\n\n" + correct)
        if addition:
            for path in addition:
                with open(path, "rb") as photo:
                    await message.answer_photo(photo=photo)

        await message.answer(final, reply_markup=inline_next)
    elif message.text in ["Завершить", "exit", "/exit", "завершить"]:
        await message.answer("Good luck")
        path = "data/end.jpg"
        with open(path, "rb") as photo:
            await message.answer_photo(
                photo=photo,
                reply_markup=keyboards.main_keyboard,
            )
        await state.finish()
    else:
        if hint and message.text in ["Подсказка", "/hint", "hint", "подсказка"]:
            await message.reply(text=hint)
        elif hint:
            await message.answer(
                "Воспользуйся подсказкой, если возникти сложности с поиском места.",
                reply_markup=keyboards.on_place,
            )
        else:
            await message.reply("Ответ не верный. Попробуй еще раз")


@dp.callback_query_handler(
    lambda c: c.data.startswith("next_question_"), state=QuestionsState.question
)
async def switch_to_next_question(call: types.CallbackQuery, state: FSMContext):
    index = int(call.data.split("_")[-1])
    await ask_next_question(call.message, state, index + 1)
    await call.message.delete_reply_markup()
