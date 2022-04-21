from bot.bot import Bot
from bot.settings import get_bot_settings
from bot.utils.keyboard import MainKeyboard, WalletsKeyboard


config = get_bot_settings().dict()
bot = Bot(**config)


@bot.commands.handle(text="hello there")
def hello_command(message: dict):
    bot.vk.messages.send(peer_id=message["from_id"], 
                         random_id=0, 
                         message="hi o/",
                         keyboard=MainKeyboard())


@bot.commands.handle(text="Кошельки")
def wallets_keyboard(message: dict):
    bot.vk.messages.send(peer_id=message["from_id"],
                         random_id=0,
                         message="Методы кошельков",
                         keyboard=WalletsKeyboard())


@bot.commands.handle(text="back_button")
def back_button_event(event: dict):
    bot.vk.messages.send(peer_id=event["peer_id"],
                         random_id=0,
                         message="goin' back",
                         keyboard=MainKeyboard())
