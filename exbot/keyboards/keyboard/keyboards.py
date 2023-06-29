from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)

registration_button = KeyboardButton(text="Регистрация", url="http://google.com")
channel_link_button = KeyboardButton(
    text="Оф. канал Telegram", url="tg://resolve?domain=telegram"
)

main_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Антиэкскурсии", callback_data="view_guides"),
            KeyboardButton(text="Список команд", callback_data=""),
        ]
    ],
)

hint_exit = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[[KeyboardButton("Подсказка"), KeyboardButton("Завершить")]],
)

complete = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[[KeyboardButton("Завершить")]],
)

next_back = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[[KeyboardButton("Следующий этап")], [KeyboardButton("Завершить")]],
)

on_place = ReplyKeyboardMarkup(
    resize_keyboard=True,
    row_width=1,
    keyboard=[
        [
            KeyboardButton("На месте"),
        ],
        [
            KeyboardButton("Подсказка"),
            KeyboardButton("Завершить"),
        ],
    ],
)
