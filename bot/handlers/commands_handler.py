from bot.utils.keyboard import MainKeyboard, WalletsKeyboard, TransactionsKeyboard
from bot.utils.redis_utils import is_registered_user
from bot.handlers.handler_config import bot
from bot.schemas.message import MessageNew
from vk_api.utils import get_random_id


def default(message: MessageNew):
    bot.vk.messages.send(peer_id=message.peer_id, 
                         random_id=get_random_id(), 
                         message="что.",
                         keyboard=MainKeyboard(is_registered_user(message.from_id)))


@bot.commands.handle_command(text="ping")
def hello_command(message: MessageNew):
    bot.vk.messages.send(peer_id=message.peer_id, 
                         random_id=get_random_id(), 
                         message="pong")


@bot.commands.handle_command(text="Кошельки")
def wallets_keyboard(message: MessageNew):
    bot.vk.messages.send(peer_id=message.peer_id,
                         random_id=get_random_id(),
                         message="Методы кошельков",
                         keyboard=WalletsKeyboard())


@bot.commands.handle_command(text="Транзакции")
def transactions_keyboard(message: MessageNew):
    bot.vk.messages.send(peer_id=message.peer_id,
                         random_id=get_random_id(),
                         message="Методы транзакций",
                         keyboard=TransactionsKeyboard())


bot.commands.default_message_handler = default
