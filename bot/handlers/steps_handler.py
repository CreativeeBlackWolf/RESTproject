from bot.handlers.handler_config import bot
from bot.api.api_requests import WalletAPIRequest, TransactionsAPIRequest
from bot.schemas.message import MessageNew
from bot.utils.keyboard import MainKeyboard, UserWalletsKeyboard, WalletsKeyboard
from bot.utils.redis_utils import is_registered_user
import json


wallets_api = WalletAPIRequest()
transactions_api = TransactionsAPIRequest()
transactions = {}


def stop_message(message: MessageNew):
    bot.vk.messages.send(peer_id=message.peer_id,
                         random_id=0,
                         message="Возвращаюсь в главное меню.",
                         keyboard=MainKeyboard(True))

def process_new_wallet(message: MessageNew):
    _, status = wallets_api.create_new_wallet(message.from_id, message.text)
    if status == 201:
        bot.vk.messages.send(peer_id=message.peer_id,
                             random_id=0,
                             message=f"Кошелёк \"{message.text}\" успешно создан!",
                             keyboard=WalletsKeyboard())
    elif status == 401:
        message = "Кошелёк с таким названием уже существует. Придумай что-нибудь другое..."
        bot.vk.messages.send(peer_id=message.peer_id,
                             random_id=0,
                             message=message,
                             keyboard=WalletsKeyboard())
    else:
        bot.vk.messages.send(peer_id=message.peer_id,
                             random_id=0,
                             message=f"Что-то пошло не так... ({status}). Сообщи об этом.",
                             keyboard=MainKeyboard())


def transactions_to_or_whence_step(message: MessageNew):
    if message.text.lower() in ("стоп", "stop"):
        stop_message(message)
        return
    global transactions
    payload = json.loads(message.payload)
    transactions[message.from_id] = {"from_wallet": payload["UUID"]}
    bot.vk.messages.send(peer_id=message.peer_id,
                         random_id=0,
                         message=f"Введи ID пользователя в ВК или куда ты хочешь перевести деньги.")
    bot.steps.register_next_step_handler(message.from_id, transactions_check_vk_id)

def transactions_check_vk_id(message: MessageNew):
    try:
        user_id = int(message.text)
        if not is_registered_user(user_id):
            bot.vk.messages.send(peer_id=message.peer_id,
                             random_id=0,
                             message="Такой пользователь не зарегистрирован в системе. Возвращаюсь.",
                             keyboard=MainKeyboard(True))
            return
        wallets, status = wallets_api.get_user_wallets(user_id)
        if status == 200:
            if not wallets:
                bot.vk.messages.send(peer_id=message.peer_id,
                             random_id=0,
                             message="У пользователя с таким ID нет кошельков. Возвращаюсь",
                             keyboard=MainKeyboard(True))
                return
            bot.vk.messages.send(peer_id=message.peer_id,
                                 random_id=0,
                                 message="Выбери кошелёк получателя.",
                                 keyboard=UserWalletsKeyboard(wallets))
            global transactions
            transactions[message.from_id]["recipient_id"] = user_id
            bot.steps.register_next_step_handler(message.from_id, transactions_payment_step)
    except ValueError:
        transactions_payment_step(message)

def transactions_payment_step(message: MessageNew):
    if message.text.lower() in ("стоп", "stop"):
        stop_message(message)
        return
    global transactions
    # if uuid is given
    if message.payload:    
        payload = json.loads(message.payload)
        transactions[message.from_id]["to_wallet"] = payload["UUID"]
        transactions[message.from_id]["whence"] = None
    else:
        transactions[message.from_id]["to_wallet"] = None
        transactions[message.from_id]["whence"] = message.text
    bot.vk.messages.send(peer_id=message.peer_id,
                         random_id=0,
                         message="Сколько перевести?")
    bot.steps.register_next_step_handler(message.from_id, transactions_comment_step)
    

def transactions_comment_step(message: MessageNew):
    if message.text.lower() in ("стоп", "stop"):
        stop_message(message)
        return
    global transactions
    try:
        transactions[message.from_id]["payment"] = int(message.text)
    except ValueError:
        bot.vk.messages.send(peer_id=message.peer_id,
                             random_id=0,
                             message="Количество переводимых средств должно быть целым числом.",
                             keyboard=MainKeyboard(True))
        return
    bot.vk.messages.send(peer_id=message.peer_id,
                         random_id=0,
                         message="Оставьте комментарий (введите \"нет\", если не нужно).")
    bot.steps.register_next_step_handler(message.peer_id, transactions_final_step)

def transactions_final_step(message: MessageNew):
    if message.text.lower() in ("стоп", "stop"):
        stop_message(message)
        return
    global transactions
    if message.text.lower() not in ("нет", "н", "no", "n"):
        transactions[message.from_id]["comment"] = message.text
    else:
        transactions[message.from_id]["comment"] = None
    transaction_data = transactions.pop(message.from_id, None)
    transaction, status = transactions_api.make_transaction(**transaction_data)
    if status == 201:
        bot.vk.messages.send(peer_id=message.peer_id,
                             random_id=0,
                             message="Перевод отправлен!",
                             keyboard=MainKeyboard(True))
        if transaction_data["recipient_id"] is not None:
            recipient = bot.vk.users.get(user_ids=message.from_id,
                                     name_case="gen")[0]
            message = \
f"""Пополнение на {transaction_data['payment']} от {recipient['first_name']} {recipient['last_name']}
Комментарий к переводу: {transaction_data['comment']}
"""
            bot.vk.messages.send(peer_id=transaction_data["recipient_id"],
                                 random_id=0,
                                 message=message)
