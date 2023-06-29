from database.base import session
from dispatcher import dp, bot
from aiogram import types, filters
# from config import PAY_TOKEN
from keyboards.inline import ikb
from database import services


@dp.callback_query_handler(lambda c: c.data.startswith("buy_excursion_"))
async def payment(call: types.CallbackQuery):
    await call.answer()
    data = call.data.split("_")
    user_id = data[-1]
    excursion_title = data[-2]
    user = await services.get_user_by_user_id(user_id=int(user_id), db=session)
    if not user:
        await call.answer("You have to register before")
        ikb.register_ikb.inline_keyboard.clear()
        ikb.register_ikb.add(*ikb.ikb)
        await call.message.edit_text(
            "Please send me your contact for registration", reply_markup=ikb.register_ikb
        )
    else:
        excursion = await services.get_excursion_by_title(excursion_title, session)
        user.excursions.extend([excursion])
        session.commit()
        ex_markup = types.InlineKeyboardMarkup(row_width=1)
        excursions_buttons = ikb.get_excursions_ikb()
        ex_markup.add(*excursions_buttons)
        await call.message.edit_text(
            text=f"Congratulate! You buy {excursion_title}",
            reply_markup=ex_markup,
        )

    # await call.message.edit_text(
    #     "Please send me your contact for registration", reply_markup=ikb.register_ikb
    # )
    # await bot.send_invoice(
    #     call.message.chat.id,
    #     "Опрлата экскурсии",
    #     "Оплата экскурсии музей",
    #     payload="invoice",
    #     # provider_token=PAY_TOKEN,
    #     currency="USD",
    #     prices=[types.LabeledPrice("Оплата экскурсии", 5 * 100)],
    # )
