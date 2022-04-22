from bot.bot import Bot
from bot.settings import get_bot_settings
from bot.utils.keyboard import MainKeyboard, WalletsKeyboard
from bot.schemas.message import MessageEvent, MessageNew


config = get_bot_settings().dict()
bot = Bot(**config)

def default(message: MessageNew):
    bot.vk.messages.send(peer_id=message.peer_id, 
                         random_id=0, 
                         message="что.",
                         keyboard=MainKeyboard())

@bot.commands.handle_command(text="hello there")
def hello_command(message: MessageNew):
    bot.vk.messages.send(peer_id=message.peer_id, 
                         random_id=0, 
                         message="hi o/",
                         keyboard=MainKeyboard())


@bot.commands.handle_command(text="Кошельки")
def wallets_keyboard(message: MessageNew):
    bot.vk.messages.send(peer_id=message.peer_id,
                         random_id=0,
                         message="Методы кошельков",
                         keyboard=WalletsKeyboard())


@bot.commands.handle_event(event="back_button")
def back_button_event(event: MessageEvent):
    bot.vk.messages.send(peer_id=event.peer_id,
                         random_id=0,
                         message="Возвращаемся в главное меню",
                         keyboard=MainKeyboard())


bot.commands.default_message_handler = default
