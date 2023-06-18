from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_menu = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="anti-excursions", callback_data="view_guides"),
        ],
    ],
)
