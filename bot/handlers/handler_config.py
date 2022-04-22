from bot.bot import Bot
from bot.settings import get_bot_settings


config = get_bot_settings().dict()
bot = Bot(**config)
