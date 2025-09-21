import logging
from aiogram import Bot
from config_reader import config
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BOT_TOKEN = config.bot_token
HOST = config.HOST
PORT = int(config.PORT)
BASE_URL = config.BASE_URL
WEBHOOK_PATH = f'/{BOT_TOKEN}'

bot = Bot(
    token=config.bot_token.get_secret_value(),
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
    )