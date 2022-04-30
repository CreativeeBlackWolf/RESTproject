from typing import Union
from bot.utils.keyboard import MainKeyboard, TransactionsKeyboard
from bot.handlers.handler_config import bot
from bot.schemas.message import MessageEvent, MessageNew
from vk_api.utils import get_random_id


def stop_message(message: Union[MessageNew, MessageEvent]):
    bot.vk.messages.send(peer_id=message.peer_id,
                         random_id=get_random_id(),
                         message="Возвращаюсь в главное меню.",
                         keyboard=MainKeyboard(True))

def error_message(message: Union[MessageNew, MessageEvent], error_message: str):
    bot.vk.messages.send(peer_id=message.peer_id,
                         random_id=get_random_id(),
                         message=f"Произошла ошибка: {error_message}",
                         keyboard=MainKeyboard(True))

def no_wallets_message(message: Union[MessageNew, MessageEvent]):
    bot.vk.messages.send(peer_id=message.peer_id,
                         random_id=get_random_id(),
                         message="Пока что у тебя нет кошельков.",
                         keyboard=TransactionsKeyboard())

def wrong_input_message(message: Union[MessageNew, MessageEvent]):
    bot.vk.messages.send(peer_id=message.peer_id,
                         random_id=get_random_id(),
                         message="Неверный ввод. Выбери нужный пункт на клавиатуре.",
                         keyboard=MainKeyboard(True))
