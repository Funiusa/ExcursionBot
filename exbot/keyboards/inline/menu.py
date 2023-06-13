from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_menu = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="alert", callback_data="alert"),
            InlineKeyboardButton(text="OK", callback_data="OK"),
        ],
        [
            InlineKeyboardButton(text="registration", url="http://google.com"),
            InlineKeyboardButton(
                text="Оф. канал Telegram", url="tg://resolve?domain=telegram"
            ),
        ],
        [
            InlineKeyboardButton(text="Excursions", callback_data="Excursions"),
        ],
    ],
)
