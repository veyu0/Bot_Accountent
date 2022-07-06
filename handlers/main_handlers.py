import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.main_kb import start_kb, all_costs_kb
from database import db
from states.state import CategoryState, NewCostState


# Хендлер для выбора задачи
async def start_point(message: types.Message):
    await message.answer(f'Приветствую вас, {message.from_user.username}, с чего начнем?', reply_markup=start_kb)


# Показать все расходы
async def all_costs(message: types.Message):
    await message.answer('Какие расходы вас интересуют?', reply_markup=all_costs_kb)


# Расходы за неделю
async def costs_week():
    pass


# Расходы за месяц
async def costs_month():
    pass


# Расходы за год
async def costs_year():
    pass


# Создать новую категорию расходов
async def new_category(message: types.Message):
    await message.answer('Какую категорию хотите добавить?')
    await CategoryState.category.set()


# Вносим категорию в базу
async def add_category(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(category=answer)

    user_id = message.from_user.id
    data = await state.get_data()
    category_name = data.get('category')

    await db.db_add_category(user_id, category_name)
    await state.finish()
    await message.answer('Категория добавлена')


# Добавить новые расходы
async def new_costs(message: types.Message):
    await message.answer('Выберите категорию расходов')
    await db.category_read(message)
    await NewCostState.category_choice.set()


# Добавление стоимости
async def add_cost(message: types.Message, state: FSMContext):
    await message.answer('Сколько вы потратили?')
    category_choice = message.text
    await state.update_data(category_choice=category_choice)
    await NewCostState.cost.set()


# Запись в БД информации о новых расходах
async def cost_to_db(message: types.Message, state: FSMContext):
    cost = message.text
    await state.update_data(cost=cost)

    user_id = message.from_user.id
    data = await state.get_data()
    category = data.get('category_choice')
    amount = data.get('cost')

    await db.db_add_record(user_id, category, amount)
    await state.finish()
    await message.answer('Добавлены новые расходы')


def register_handlers_main(dp: Dispatcher):
    dp.register_message_handler(start_point, commands=['start'])
    dp.register_message_handler(new_costs, commands=['Добавить_новые_расходы'])
    dp.register_message_handler(add_cost, state=NewCostState.category_choice)
    dp.register_message_handler(cost_to_db, state=NewCostState.cost)
    dp.register_message_handler(new_category, commands=['Добавить_категорию'])
    dp.register_message_handler(add_category, state=CategoryState.category)
    dp.register_message_handler(all_costs, commands=['Просмотр_расходов'])
    dp.register_message_handler(costs_week, commands=['За_неделю'])
    dp.register_message_handler(costs_month, commands=['За_месяц'])
    dp.register_message_handler(costs_year, commands=['За_год'])
