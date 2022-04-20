from vkbottle import Bot, Callback, GroupEventType, GroupTypes, Keyboard, ShowSnackbarEvent, KeyboardButtonColor
from vkbottle.bot import Message
from vkbottle.callback import BotCallback
from bot.settings import get_bot_settings
from bot.utils.keyboard import KEYBOARD

config = get_bot_settings()

TOKEN = config.token
callback = BotCallback(url=config.url, title="WalletBot")
bot = Bot(token=TOKEN, callback=callback)


@bot.on.message(text="info")
async def send_callback_button(message: Message):
    await message.answer(keyboard=KEYBOARD, message="fuck you")

