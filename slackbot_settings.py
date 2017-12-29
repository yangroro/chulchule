from os import environ
from os.path import join, dirname, abspath

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.myenv')
load_dotenv(dotenv_path)

API_TOKEN = environ.get('SLACK_API_TOKEN')
ERRORS_TO = environ.get('DEFAULT_ERROR_REPORT')

DEFAULT_REPLY = "출출해.."

ROOT_DIR = dirname(abspath(__file__))

PLUGINS = [
    'chulchule_bot.plugins.tester',
    'chulchule_bot.plugins.late_counter',
]
