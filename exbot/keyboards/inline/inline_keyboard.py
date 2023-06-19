from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_help = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="anti-excursions", callback_data="view_guides"),
        ],
    ],
)
on_place = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="На месте", callback_data="get_question"),
        ],
    ],
)

menu = InlineKeyboardMarkup(
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
            InlineKeyboardButton(text="Anti-excursions", callback_data="view_guides"),
        ],
    ],
)
