from bot.utils.keyboard import MainKeyboard, WalletsKeyboard, TransactionsKeyboard
from bot.utils.redis_utils import is_registered_user
from bot.handlers.handler_config import bot
from bot.schemas.message import MessageNew


@bot.commands.default_handler
def default(message: MessageNew):
    bot.send_message(message, 
                     text="что.",
                     keyboard=MainKeyboard(is_registered_user(message.from_id)))


@bot.commands.handle_command(text="ping")
def hello_command(message: MessageNew):
    bot.send_message(message,
                     text="pong!")


@bot.commands.handle_command(text="Кошельки")
def wallets_keyboard(message: MessageNew):
    bot.send_message(message,
                     text="Методы кошельков",
                     keyboard=WalletsKeyboard())


@bot.commands.handle_command(text="Транзакции")
def transactions_keyboard(message: MessageNew):
    bot.send_message(message, 
                     text="Методы транзакций",
                     keyboard=TransactionsKeyboard())
