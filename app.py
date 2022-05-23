from aiogram import executor

from data.config import WEBHOOK
from loader import dp, bot
from utils.set_bot_commands import set_default_commands
from service.database.create import create_database
from service.database.api import DatabaseApi
import handlers


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Create database tables if not exists
    await create_database()
    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
