import psycopg2
from aiogram import executor

from data.config import *
from loader import dp
import handlers # middlewares, filters,
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    pass
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

#
#
# try:
#     connection = psycopg2.connect(
#         host = host,
#         user = user,
#         password = password,
#         database = db_name
#     )
#
#     cursor = connection.cursor()
#
#     with connection.cursor() as cur:
#         cur.execute(
#             'SELECT * FROM loop;'
#         )
#         print(66, cur.fetchone())
# except Exception as _ex:
#     print(['kmlmmlm'], _ex)
# finally:
#     pass
#     if connection:
#         connection.close()
#         print('[INFO] PostgreSQL closed')



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)

