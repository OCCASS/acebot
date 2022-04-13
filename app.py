from aiogram import executor

from loader import dp
from utils.set_bot_commands import set_default_commands
from service.database.create import create_database
import middlewares, filters, handlers


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Create database tables if not exists
    await create_database()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
