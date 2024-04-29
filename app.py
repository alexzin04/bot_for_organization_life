from datetime import datetime, timedelta
from aiogram import executor

from loader import dp,scheduler
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.tasks_reapeats import every_day_helper
from utils.db_api.create_all_db import create_new_db




async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)
    if (input('Перезапускаем базу данных - 1 если да\n')=='1'):
        create_new_db()
    scheduler.add_job(every_day_helper, 'cron', hour=4, minute=00,timezone='Europe/Moscow')
    await every_day_helper()
    # Уведомляет про запуск
    #await on_startup_notify(dispatcher)


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)
