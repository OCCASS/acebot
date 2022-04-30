from pathlib import Path

from environs import Env

from utils.load_bad_words import load_bad_words

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
POSTGRESQL_URI = env.str("POSTGRESQL_URI")
ADMINS = list(map(int, env.list('ADMINS')))
WEBHOOK = env.str('WEBHOOK')

BASE_DIR = Path(__file__).parent.parent

I18N_DOMAIN = 'acebot'
I18N_PATH = BASE_DIR / 'locales'

BAD_WORDS_PATH = BASE_DIR / 'bad_words'
BAD_WORDS = load_bad_words()

STATES_FILE_NAME = 'states.json'
STATES_PATH = BASE_DIR / STATES_FILE_NAME

CIS_COUNTRIES = ['Россия', 'Армения', 'Беларусь', 'Казахстан', 'Кыргызстан', 'Таджикистан', 'Туркменистан',
                 'Узбекистан', 'Украина', 'Азербайджан', 'Молдова']

DAYS_IN_MONTH = 30
WARNING_AGE = 16
COMPLAINS_COUNT_TO_NOTIFY_ADMINS = 3
RATE_LIMIT = .3
