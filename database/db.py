import sqlite3 as sq
from create_bot import bot


def start_db():
    global base, cur
    base = sq.connect('accountent.db')
    cur = base.cursor()
    if base:
        print('Database is working!')

    base.execute('CREATE TABLE IF NOT EXISTS categories(user_id INT, category TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS records(user_id INT, category TEXT, amount TEXT, data DATE DEFAULT CURRENT_DATE, FOREIGN KEY (category) REFERENCES categories(category))')
    base.commit()


async def db_add_category(user_id: int, category: str):
    cur.execute('INSERT INTO categories (user_id, category) VALUES (?, ?)', (user_id, category))
    base.commit()


async def category_read(message):
    user_id = message.from_user.id
    for cat in cur.execute(f'SELECT category FROM categories WHERE user_id = {user_id}').fetchall():
        await message.answer(f'Категория - {cat[0]}')


async def db_add_record(user_id: int, category: str, amount: int):
    cur.execute('INSERT INTO records (user_id, category, amount) VALUES (?, ?, ?)', (user_id, category, amount))
    base.commit()


async def costs_week_read(message):
    user_id = message.from_user.id
    for cat, cost, date in cur.execute(f'SELECT category, amount, data FROM records WHERE user_id = {user_id} AND data >= date("now", "-7 days")').fetchall():
        await message.answer(f'Категория - {cat}, потрачено - {cost}')
    for final_cost in cur.execute(f'SELECT SUM(amount) FROM records').fetchall():
        await message.answer(f'Всего за неделю вы потратили - {final_cost[0]}')


async def costs_month_read(message):
    user_id = message.from_user.id
    for cat, cost, date in cur.execute(f'SELECT category, amount, data FROM records WHERE user_id = {user_id} AND data >= date("now", "-1 month")').fetchall():
        await message.answer(f'Категория - {cat}, потрачено - {cost}')
    for final_cost in cur.execute(f'SELECT SUM(amount) FROM records').fetchall():
        await message.answer(f'Всего за месяц вы потратили - {final_cost[0]}')


async def costs_year_read(message):
    user_id = message.from_user.id
    for cat, cost, date in cur.execute(f'SELECT category, amount, data FROM records WHERE user_id = {user_id} AND data >= date("now", "-1 year")').fetchall():
        await message.answer(f'Категория - {cat}, потрачено - {cost}')
    for final_cost in cur.execute(f'SELECT SUM(amount) FROM records').fetchall():
        await message.answer(f'Всего за год вы потратили - {final_cost[0]}')
