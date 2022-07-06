from create_bot import dp
from aiogram.utils import executor
from handlers import main_handlers
from database import db


async def on_startup(_):
    print('Бот запущен')
    db.start_db()

main_handlers.register_handlers_main(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
