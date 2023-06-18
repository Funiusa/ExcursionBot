from aiogram.dispatcher.filters.state import StatesGroup, State


class QuestionsState(StatesGroup):
    question = State()
