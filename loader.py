from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.files import JSONStorage

from data import config
from filters.admin_filter import IsAdmin
from middlewares.i18n import LanguageMiddleware
from middlewares.throttling import ThrottlingMiddleware
from middlewares.banned_users import BannedUsersMiddleware
from middlewares.user_info_change import UserInfoChangedMiddleware
from service.database.api import DatabaseApi
from utils.logging import init_logger

init_logger()

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = JSONStorage(config.STATES_PATH)
dp = Dispatcher(bot, storage=storage)
db = DatabaseApi()

# Config i18n middleware
i18n = LanguageMiddleware(config.I18N_DOMAIN, config.I18N_PATH)
dp.middleware.setup(i18n)

_ = i18n.gettext

# Config throttling middleware
dp.middleware.setup(ThrottlingMiddleware())

# Config banned users middleware
dp.middleware.setup(BannedUsersMiddleware())

# Config user info checker
dp.middleware.setup(UserInfoChangedMiddleware())


dp.bind_filter(IsAdmin())
