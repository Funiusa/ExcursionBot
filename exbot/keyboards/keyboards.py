from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

registration_inline_button = InlineKeyboardButton(
    text="Регистрация", url="http://google.com"
)
channel_inline_link = InlineKeyboardButton(
    text="Оф. канал Telegram", url="tg://resolve?domain=telegram"
)
excursions_inline_button = InlineKeyboardButton(
    text="Экскурсии", callback_data="view_guides"
)


inline_main_menu = [
    registration_inline_button,
    channel_inline_link,
    excursions_inline_button,
]

exit_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True
)
iexit_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]
    ]
)

builder = InlineKeyboardMarkup(row_width=5)

registration_button = KeyboardButton(text="Регистрация", url="http://google.com")
channel_link_button = KeyboardButton(
    text="Оф. канал Telegram", url="tg://resolve?domain=telegram"
)

excursions_button = KeyboardButton(text="Антиэкскурсии", callback_data="view_guides")
all_commands_button = KeyboardButton(text="Список команд", callback_data="")

main_buttons = [
    excursions_button,
    all_commands_button,
]
replay_main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
replay_main_keyboard.add(*main_buttons)
