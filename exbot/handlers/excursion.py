from aiogram import types
import keyboards
import text
from dispatcher import dp, bot


@dp.message_handler(regexp="Экскурсии")
@dp.message_handler(commands=["excursions"])
async def excursions_handler(message: types.Message):
    await send_guide_list(message.chat.id, message.from_user.first_name)


@dp.callback_query_handler(lambda c: c.data == "view_guides")
async def view_guides_handler(callback_query: types.CallbackQuery):
    await send_guide_list(
        callback_query.message.chat.id, callback_query.from_user.first_name
    )


async def send_guide_list(chat_id, user_name):
    keyboard = types.InlineKeyboardMarkup()
    number_of_excursion = len(text.guides)
    for guide in text.guides:
        title = guide["title"]
        button = types.InlineKeyboardButton(title, callback_data=f"view_guide_{title}")
        keyboard.add(button)
    photo_path = "data/girl_and_burning_house.jpg"
    with open(photo_path, "rb") as photo:
        await bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=text.greet.format(name=user_name),
        )
    await bot.send_message(
        chat_id=chat_id,
        text=text.excursion_greet.format(name=user_name, number=number_of_excursion),
        reply_markup=keyboard,
    )


@dp.callback_query_handler(lambda c: c.data.startswith("view_guide_"))
async def view_guide_handler(callback_query: types.CallbackQuery):
    data = callback_query.data.split("_")
    guide_title = " ".join(data[2:])
    guide = next((g for g in text.guides if g["title"] == guide_title), None)
    keyboard = types.InlineKeyboardMarkup()
    begin_guide_button = types.InlineKeyboardButton(
        "Let's begin?", callback_data=f"question_{guide_title}_0"
    )
    if guide:
        await bot.send_message(
            callback_query.from_user.id,
            text=guide.get("greet"),
        )
        image_path = guide.get("image")
        with open(image_path, "rb") as photo:
            keyboard.add(begin_guide_button)
            await bot.send_photo(
                chat_id=callback_query.message.chat.id,
                photo=photo,
                caption=f"\n\n{guide['description']}",  # max length 1024
                reply_markup=keyboard,
            )
    else:
        await bot.send_message(callback_query.from_user.id, "Guide not found.")


@dp.callback_query_handler(lambda c: c.data.startswith("question_"))
async def send_question(callback_query: types.CallbackQuery):
    data = callback_query.data.split("_")
    guide_title = data[1]
    question_index = int(data[2])
    chat_id = callback_query.message.chat.id
    try:
        question = text.questions[guide_title][question_index]
        question_text = question["question"]
        options = question["options"]
        image_path = question.get("image")
        if image_path:
            with open(image_path, "rb") as photo:
                await bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=f"\n\n{question['text']}",  # max length 1024
                )
        else:
            await bot.send_message(
                chat_id=chat_id,
                text=f"\n\n{question['text']}",
            )
        keyboard = types.InlineKeyboardMarkup()
        for option in options:
            button = types.InlineKeyboardButton(
                option,
                callback_data=f"answer_{guide_title}_{question_index}_{option}",
            )
            keyboard.add(button)
        await bot.send_message(chat_id, question_text, reply_markup=keyboard)
    except IndexError:
        await guide_finale(callback_query.from_user.id, guide_title)


@dp.callback_query_handler(lambda c: c.data.startswith("answer_"))
async def answer_handler(callback_query: types.CallbackQuery):
    data = callback_query.data.split("_")
    guide_title = data[1]
    question_index = int(data[2])
    chosen_option = data[3]

    question = text.questions[guide_title][question_index]
    correct_answer = question["answer"]
    answer = (
        question["correct"] if chosen_option == correct_answer else question["wrong"]
    )
    next_keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(
        text="Идем дальше?",
        callback_data=f"question_{guide_title}_{question_index + 1}",
    )
    next_keyboard.add(button)
    await bot.send_message(
        callback_query.from_user.id,
        text=answer,
        reply_markup=next_keyboard,
    )


async def guide_finale(user_id, guide_title):
    main_keyboard = types.InlineKeyboardMarkup()
    main_keyboard.add(*keyboards.inline_main_menu)
    guide = next((g for g in text.guides if g["title"] == guide_title), None)
    image_path = guide.get("final_image")
    if image_path:
        with open(image_path, "rb") as photo:
            await bot.send_photo(
                user_id,
                photo,
                guide.get("final"),
                reply_markup=main_keyboard,
            )
    else:
        await bot.send_message(
            user_id,
            f"{guide.get('final')} '{guide['title']}'.",
            reply_markup=main_keyboard,
        )
