import os
from asyncio import sleep
from typing import List

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State

from content.excursions_list import guides
from content.questions import questions
from dispatcher import dp, bot
from keyboards import keyboards
from state import QuestionsState


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


def get_addition_data(title: str, index: int) -> list:
    path = f"data/{title}/{index}"
    files = []

    if os.path.exists(path):
        for root, _, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                files.append(file_path)
    return files


async def ask_next_question(message: types.Message, state: FSMContext, index: int):
    data = await state.get_data()
    question = data["questions"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    hint_button = types.KeyboardButton("Подсказка")
    end_button = types.KeyboardButton("Завершить")
    keyboard.add(hint_button, end_button)
    try:
        image_path = question[index]["image"]
        if image_path:
            with open(image_path, "rb") as photo:
                await bot.send_photo(
                    chat_id=message.chat.id, photo=photo, reply_markup=keyboard
                )
            answer = question[index]["answer"]
            hint = question[index]["hint"]
            correct = question[index]["correct"]
            end_question = question[index]["end"]
            folder_name = question[index]["addition"]
            addition = get_addition_data(folder_name, index + 1)
            await state.update_data(
                answer=answer,
                hint=hint,
                correct=correct,
                end=end_question,
                addition=addition,
                index=index,
            )
            await QuestionsState.question.set()
            await message.answer("Вводи ответ тут и жми отправить!")
    except IndexError:
        await message.answer("Вы прошли ознокомительный блок")
        path = "data/end.jpg"
        with open(path, "rb") as photo:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                reply_markup=keyboards.replay_main_keyboard,
            )
        await state.finish()


def clear_answer(line: str) -> str:
    import re

    answer = "".join(re.findall(r"\b\w+\b", line)).lower()
    return answer


@dp.message_handler(state=QuestionsState.question)
async def answer_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    correct_answer = data["answer"]
    hint = data["hint"]
    index = data["index"]
    correct = data["correct"]
    end_question = data["end"]
    addition = data["addition"]
    answer = clear_answer(message.text)
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
                reply_markup=keyboards.replay_main_keyboard,
            )
        await state.finish()
    else:
        if hint and message.text in ["Подсказка", "/hint", "hint", "for подсказка"]:
            with open(hint, "rb") as photo:
                # await message.answer_photo(photo=photo, reply_markup=keyboard)
                await message.reply_photo(photo=photo)
        else:
            await message.answer("Ответ не верный. Попробуй еще раз")


@dp.callback_query_handler(
    lambda c: c.data.startswith("next_question"), state=QuestionsState.question
)
async def switch_to_next_question(call: types.CallbackQuery, state: FSMContext):
    index = int(call.data.split("_")[-1])
    await ask_next_question(call.message, state, index + 1)
