from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from middlewares.i18n import LanguageMiddleware
from middlewares.throttling import ThrottlingMiddleware
from service.database.api import DatabaseApi

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = DatabaseApi()

# Config i18n middleware
i18n = LanguageMiddleware(config.I18N_DOMAIN, config.I18N_PATH)
dp.middleware.setup(i18n)

_ = i18n.gettext

# Config throttling middleware
dp.middleware.setup(ThrottlingMiddleware())
