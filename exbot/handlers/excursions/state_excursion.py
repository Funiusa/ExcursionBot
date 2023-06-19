from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext

from content.excursions_list import guides
from content.questions import questions
from dispatcher import dp, bot
from keyboards.keyboard import keyboards
from keyboards.inline import inline_keyboard
from state import QuestionsState
from utils.data import get_addition_data, clear_answer


@dp.callback_query_handler(lambda c: c.data.startswith("view_guide_"))
async def guide_description_handler(callback_query: types.CallbackQuery):
    data = callback_query.data.split("_")
    guide_title = " ".join(data[2:])
    guide = next((g for g in guides if g["title"] == guide_title), None)

    keyboard = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton(
        "Вернуться к списку", callback_data="view_guides"
    )
    choose_button = types.InlineKeyboardButton(
        "Пройти", callback_data=f"guide_{guide_title}"
    )
    keyboard.add(back_button, choose_button)
    if guide:
        await bot.send_message(
            callback_query.from_user.id,
            text=guide["description"],
            reply_markup=keyboard,
        )
    else:
        await bot.send_message(callback_query.from_user.id, "Guide not found.")


@dp.callback_query_handler(lambda c: c.data.startswith("guide_"))
async def guide_introduction_handler(callback_query: types.CallbackQuery):
    data = callback_query.data.split("_")
    guide_title = data[1]
    guide = next((g for g in guides if g["title"] == guide_title), None)
    keyboard = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton(
        "Вернуться к списку", callback_data="view_guides"
    )
    start_button = types.InlineKeyboardButton(
        "Задание", callback_data=f"question_{guide_title}"
    )
    keyboard.add(back_button, start_button)
    image_path = guide.get("image")
    greet = guide.get("greet")
    if image_path:
        with open(image_path, "rb") as photo:
            await bot.send_photo(
                chat_id=callback_query.message.chat.id,
                photo=photo,
                caption=greet,  # max length 1024
                reply_markup=keyboard,
            )
    else:
        await bot.send_message(
            chat_id=callback_query.message.chat.id,
            text=greet,
            reply_markup=keyboard,
        )


@dp.callback_query_handler(lambda c: c.data.startswith("question_"))
async def start_handler(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data.split("_")
    guide_title = data[1]
    guide_questions = questions.get(guide_title)
    index = 0
    await state.update_data(questions=guide_questions)
    await ask_next_question(message=callback_query.message, state=state, index=index)


async def ask_next_question(message: types.Message, state: FSMContext, index: int):
    data = await state.get_data()
    question = data["questions"]
    try:
        place_image = question[index]["place"]
        if place_image:
            with open(place_image, "rb") as photo:
                await bot.send_photo(
                    chat_id=message.chat.id,
                    reply_markup=keyboards.on_place,
                    photo=photo,
                )
            folder_name = question[index]["addition"]
            await state.update_data(
                index=index,
                end=question[index]["end"],
                hint=question[index]["hint"],
                answer=question[index]["answer"],
                correct=question[index]["correct"],
                question=question[index]["question"],
                addition=get_addition_data(folder_name, index + 1),
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
    path = data["question"]
    with open(path, "rb") as image:
        await message.answer_photo(photo=image)
    await state.update_data(hint=None)

    await message.answer(
        "Вводи ответ тут и жми отправить!", reply_markup=keyboards.back
    )


@dp.message_handler(state=QuestionsState.question)
async def answer_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    correct_answer = data["answer"]
    hint = data["hint"]
    index = data["index"]
    correct = data["correct"]
    end_question = data["end"]
    addition = data["addition"]
    answer = clear_answer(str(message.text))
    inline_next = types.InlineKeyboardMarkup()

    next_question = types.InlineKeyboardButton(
        "Следующий этап", callback_data=f"next_question_{index}"
    )
    inline_next.add(next_question)

    if answer == correct_answer:
        await message.answer("Ответ правильный!:)")
        await message.answer(correct)
        if addition:
            for path in addition:
                with open(path, "rb") as photo:
                    await message.answer_photo(photo=photo)

        await sleep(2)
        await message.answer(end_question, reply_markup=inline_next)
    elif message.text in ["Завершить", "exit", "/exit", "завершить"]:
        await message.answer("Good luck")
        path = "data/end.jpg"
        with open(path, "rb") as photo:
            await bot.send_photo(
                chat_id=message.chat.id,
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
                reply_markup=keyboards.hint_exit,
            )
        else:
            await message.answer("Ответ не верный. Попробуй еще раз")


@dp.callback_query_handler(
    lambda c: c.data.startswith("next_question_"), state=QuestionsState.question
)
async def switch_to_next_question(call: types.CallbackQuery, state: FSMContext):
    index = int(call.data.split("_")[-1])
    await ask_next_question(call.message, state, index + 1)
    await call.message.delete_reply_markup()
