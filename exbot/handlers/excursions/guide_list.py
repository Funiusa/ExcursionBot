from aiogram import types, filters
from sqlalchemy import select

from database.base import session
from database import services
from database.services import get_excursion_by_title
from dispatcher import dp, bot
from content import greet
from keyboards.inline import ikb


@dp.message_handler(text="Антиэкскурсии")
@dp.message_handler(commands=["anti_excursions"])
async def excursions_list(message: types.Message):
    ex_markup = types.InlineKeyboardMarkup(row_width=1)
    excursions_buttons = ikb.get_excursions_ikb()
    ex_markup.add(*excursions_buttons)
    if excursions_buttons:
        await message.answer(
            text=greet.excursion_greet.format(
                name=message.from_user.username, number=len(excursions_buttons)
            ),
            reply_markup=ex_markup,
        )
    else:
        await message.answer("There isn't any excursions yet")


@dp.callback_query_handler(filters.Text("guides_list"))
async def show_excursions(call: types.CallbackQuery):
    ex_markup = types.InlineKeyboardMarkup(row_width=1)
    excursions_buttons = ikb.get_excursions_ikb()
    ex_markup.add(*excursions_buttons)
    await call.message.edit_text(
        text=greet.excursion_greet.format(
            name=call.from_user.username, number=len(excursions_buttons)
        ),
        reply_markup=ex_markup,
    )


@dp.callback_query_handler(filters.Text("guides_main"))
async def show_excursions_main(call: types.CallbackQuery):
    await call.answer()
    ex_markup = types.InlineKeyboardMarkup(row_width=1)
    excursions_buttons = ikb.get_excursions_ikb()
    ex_markup.add(*excursions_buttons, ikb.back_to_main_menu)
    await call.message.edit_text(
        text=greet.excursion_greet.format(
            name=call.from_user.username, number=len(excursions_buttons)
        ),
        reply_markup=ex_markup,
    )


@dp.callback_query_handler(lambda c: c.data.startswith("guides_end_"))
async def show_excursions_end(call: types.CallbackQuery):
    await call.message.delete()
    data = call.data.split("_")
    title = data[-2]
    message_id = data[-1]
    ex_markup = types.InlineKeyboardMarkup(row_width=1)
    excursions_buttons = types.InlineKeyboardButton(text=f"guide_detail_{title}")
    ex_markup.add(excursions_buttons)
    await bot.edit_message_text(
        text=greet.excursion_greet,
        chat_id=call.message.chat.id,
        message_id=message_id,
        reply_markup=ex_markup
    )


excursion_ikb = types.InlineKeyboardMarkup()


@dp.callback_query_handler(lambda c: c.data.startswith("guide_detail_"))
async def excursion_detail(call: types.CallbackQuery):
    user_id = call.from_user.id
    title = call.data.split("_")[-1]
    user = await services.get_user_by_user_id(user_id=user_id, db=session)

    excursion = await get_excursion_by_title(title=title, db=session)

    back_button = types.InlineKeyboardButton(
        "Назад", callback_data="guides_list"
    )
    if user and title in [ex.title for ex in user.excursions]:
        choose_button = types.InlineKeyboardButton(
            "Пройти", callback_data=f"guide_{title}"
        )
    else:
        choose_button = types.InlineKeyboardButton(
            "Купить 💳", callback_data=f"buy_excursion_{title}_{user_id}"
        )
    excursion_ikb.inline_keyboard.clear()
    excursion_ikb.add(back_button, choose_button)
    await call.message.edit_text(
        text=excursion.intro,
        reply_markup=excursion_ikb,
    )
