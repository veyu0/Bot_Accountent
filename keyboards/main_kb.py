from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_kb_1 = KeyboardButton('/Добавить_новые_расходы')
start_kb_2 = KeyboardButton('/Добавить_категорию')
start_kb_3 = KeyboardButton('/Просмотр_расходов')

start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
start_kb.add(start_kb_3).add(start_kb_2).add(start_kb_1)


all_costs_kb1 = KeyboardButton('/За_неделю')
all_costs_kb2 = KeyboardButton('/За_месяц')
all_costs_kb3 = KeyboardButton('/За_год')

all_costs_kb = ReplyKeyboardMarkup(resize_keyboard=True)
all_costs_kb.add(all_costs_kb1).add(all_costs_kb2).add(all_costs_kb3)

