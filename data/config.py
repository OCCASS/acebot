from pathlib import Path

from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
POSTGRESQL_URI = env.str("POSTGRESQL_URI")

BASE_DIR = Path(__file__).parent.parent

I18N_DOMAIN = 'acebot'
I18N_PATH = BASE_DIR / 'locales'

CIS_COUNTRIES = ['Россия', 'Армения', 'Беларусь', 'Казахстан', 'Кыргызстан', 'Таджикистан', 'Туркменистан',
                 'Узбекистан', 'Украина', 'Азербайджан', 'Молдова']

DAYS_IN_MONTH = 30
