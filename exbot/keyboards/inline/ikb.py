from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import crud
from database.base import async_session

inline_help = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="anti-excursions", callback_data="guides"),
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


registration_ikb = (
    InlineKeyboardButton(text="Регистрация", callback_data="registration_block"),
)

main_menu = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Антиэкскурсии", callback_data="guides_main"),
        ],
        [
            InlineKeyboardButton(text="Помощь", callback_data="help_block"),
            InlineKeyboardButton(text="Список команд", callback_data="commands_list"),
        ],
        [*registration_ikb],
    ],
)

back_to_main_menu = InlineKeyboardButton(
    text="« back to main", callback_data="start_block"
)

register_ikb = InlineKeyboardMarkup(row_width=1)
ikb = [
    InlineKeyboardButton(text="Зарегистрироваться", callback_data="registration_state"),
    InlineKeyboardButton(text="Отмена", callback_data="remove_ikb"),
]


async def get_excursions_ikb() -> list[InlineKeyboardButton]:
    guides = await crud.excursions.get_excursions(db=async_session)
    guide_ikb = [
        InlineKeyboardButton(g.title, callback_data=f"guide_detail_{g.title}")
        for g in guides
        if g.is_published
    ]
    return guide_ikb
