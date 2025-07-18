from aiogram import Bot
from config_reader import config
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

bot = Bot(
    token=config.bot_token.get_secret_value(),
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
    )