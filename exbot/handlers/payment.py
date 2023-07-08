from aiogram import filters, types

from database import crud
from database.base import db
from dispatcher import bot, dp

# from config import PAY_TOKEN
from keyboards.inline import ikb


@dp.callback_query_handler(lambda c: c.data.startswith("buy_excursion_"))
async def payment(call: types.CallbackQuery):
    await call.answer()
    data = call.data.split("_")
    telegram_id = data[-1]
    excursion_title = data[-2]
    user = await crud.users.get_user_by_telegram_id(telegram_id=int(telegram_id), db=db)
    if not user:
        await call.answer("You have to register before")
        ikb.register_ikb.inline_keyboard.clear()
        ikb.register_ikb.add(*ikb.ikb)
        await call.message.edit_text(
            "Please send me your contact for registration",
            reply_markup=ikb.register_ikb,
        )
    else:
        excursion = await crud.excursions.get_excursion_by_title(excursion_title, db)
        user.excursions.extend([excursion])
        await db.commit()
        ex_markup = types.InlineKeyboardMarkup(row_width=1)
        excursions_buttons = await ikb.get_excursions_ikb()
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
