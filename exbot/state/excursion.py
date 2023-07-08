from aiogram.dispatcher.filters.state import State, StatesGroup


class QuestionsState(StatesGroup):
    question = State()
