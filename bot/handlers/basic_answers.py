from typing import Union
from bot.utils.keyboard import MainKeyboard, TransactionsKeyboard
from bot.handlers.handler_config import bot
from bot.schemas.message import MessageEvent, MessageNew


def stop_message(message: Union[MessageNew, MessageEvent]):
    bot.send_message(message,
                     text="Возвращаюсь в главное меню.",
                     keyboard=MainKeyboard(True))

def error_message(message: Union[MessageNew, MessageEvent], error_message: str):
    bot.send_message(message,
                     text=f"Произошла ошибка: {error_message}",
                     keyboard=MainKeyboard(True))

def no_wallets_message(message: Union[MessageNew, MessageEvent]):
    bot.send_message(message,
                     text="Пока что у тебя нет кошельков.",
                     keyboard=TransactionsKeyboard())

def wrong_input_message(message: Union[MessageNew, MessageEvent]):
    bot.send_message(message,
                     text="Неверный ввод. Выбери нужный пункт на клавиатуре.",
                     keyboard=MainKeyboard(True))