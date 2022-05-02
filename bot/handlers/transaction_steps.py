from bot.api.api_requests import WalletAPIRequest, TransactionsAPIRequest
from bot.utils.keyboard import MainKeyboard, UserWalletsKeyboard
from bot.utils.redis_utils import is_registered_user
from bot.handlers.basic_answers import stop_message, wrong_input_message
from bot.handlers.handler_config import bot
from bot.schemas.message import MessageNew
from bot.utils.check import find_urls
import json


wallets_api = WalletAPIRequest()
transactions_api = TransactionsAPIRequest()
transactions = {}


def transactions_to_or_whence_step(message: MessageNew):
    if message.text.lower() in ("стоп", "stop"):
        stop_message(message)
        return

    if message.payload:
        payload = json.loads(message.payload)
    else:
        wrong_input_message(message)
        return

    transactions[message.from_id] = {"from_wallet": payload["UUID"]}
    bot.send_message(message,
        text="Введи ID пользователя в ВК (можно ссылкой) или куда ты хочешь перевести деньги."
    )
    bot.steps.register_next_step_handler(message.from_id, transactions_check_vk_id)

def transactions_check_vk_id(message: MessageNew):
    try:
        if urls := find_urls(message.text):
            for url in urls:
                if "vk.com/" in url:
                    user = bot.vk.users.get(user_ids=url.split("/")[-1])[0]
                    if not user:
                        bot.send_message(message,
                            message="Ссылка введена неверно или такого пользователя не существует",
                            keyboard=MainKeyboard(True)
                        )
                        return
                    user_id = user["id"]

        else:
            user_id = int(message.text)
        if not is_registered_user(user_id):
            bot.send_message(message,
                             text="Такой пользователь не зарегистрирован в системе. Возвращаюсь.",
                             keyboard=MainKeyboard(True))
            return
        
        wallets, status = wallets_api.get_user_wallets(user_id)
        if status == 200:
            if not wallets:
                bot.send_message(message,
                                 text="У пользователя с таким ID нет кошельков. Возвращаюсь",
                                 keyboard=MainKeyboard(True))
                return
            bot.send_message(message,
                             text="Выбери кошелёк получателя.",
                             keyboard=UserWalletsKeyboard(wallets))
    
            transactions[message.from_id]["recipient_id"] = user_id
            bot.steps.register_next_step_handler(message.from_id, transactions_payment_step)
    except ValueError:
        transactions[message.from_id]["recipient_id"] = None
        transactions_payment_step(message)

def transactions_payment_step(message: MessageNew):
    if message.text.lower() in ("стоп", "stop"):
        stop_message(message)
        return
    # if uuid is given
    if message.payload:    
        payload = json.loads(message.payload)
        transactions[message.from_id]["to_wallet"] = payload["UUID"]
        transactions[message.from_id]["whence"] = None
    else:
        transactions[message.from_id]["to_wallet"] = None
        transactions[message.from_id]["whence"] = message.text
    bot.send_message(message,
                     text="Сколько перевести?")
    bot.steps.register_next_step_handler(message.from_id, transactions_comment_step)

def transactions_comment_step(message: MessageNew):
    if message.text.lower() in ("стоп", "stop"):
        stop_message(message)
        return
    try:
        transactions[message.from_id]["payment"] = int(message.text)
    except ValueError:
        bot.send_message(message,
                         text="Количество переводимых средств должно быть целым числом.",
                         keyboard=MainKeyboard(True))
        return
    bot.send_message(message,
                     text="Оставьте комментарий (введите \"нет\", если не нужно).")
    bot.steps.register_next_step_handler(message.peer_id, transactions_final_step)

def transactions_final_step(message: MessageNew):
    if message.text.lower() in ("стоп", "stop"):
        stop_message(message)
        return
    if message.text.lower() not in ("нет", "н", "no", "n"):
        transactions[message.from_id]["comment"] = message.text
    else:
        transactions[message.from_id]["comment"] = None
    transaction_data = transactions.pop(message.from_id, None)
    _, status = transactions_api.make_transaction(**transaction_data)
    if status == 201:
        bot.send_message(message,
                         text="Перевод отправлен!",
                         keyboard=MainKeyboard(True))
        if transaction_data["recipient_id"] is not None:
            recipient = bot.vk.users.get(user_ids=message.from_id,
                                     name_case="gen")[0]
            text = \
f"""Пополнение на {transaction_data['payment']} от {recipient['first_name']} {recipient['last_name']}
Комментарий к переводу: {transaction_data['comment']}
"""
            bot.send_message(message,
                             text=text,
                             peer_id=transaction_data["recipient_id"])
