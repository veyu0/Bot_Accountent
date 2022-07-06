from aiogram.dispatcher.filters.state import StatesGroup, State


class CategoryState(StatesGroup):
    category = State()


class NewCostState(StatesGroup):
    category_choice = State()
    cost = State()