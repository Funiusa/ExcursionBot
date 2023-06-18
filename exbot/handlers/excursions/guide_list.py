from aiogram import types
from dispatcher import dp, bot
from content.excursions_list import guides
from content import greet


@dp.message_handler(text="Антиэкскурсии")
@dp.message_handler(commands=["anti_excursions"])
async def excursions_handler(message: types.Message):
    await send_guide_list(message.chat.id, message.from_user.first_name)


@dp.callback_query_handler(lambda c: c.data == "view_guides")
async def view_guides_handler(callback_query: types.CallbackQuery):
    await send_guide_list(
        callback_query.message.chat.id, callback_query.from_user.first_name
    )


async def send_guide_list(chat_id, user_name):
    keyboard = types.InlineKeyboardMarkup()
    number_of_excursion = len(guides)
    for guide in guides:
        title = guide["title"]
        button = types.InlineKeyboardButton(title, callback_data=f"view_guide_{title}")
        keyboard.add(button)
    await bot.send_message(
        chat_id=chat_id,
        text=greet.excursion_greet.format(name=user_name, number=number_of_excursion),
        reply_markup=keyboard,
    )
