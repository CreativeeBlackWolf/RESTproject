from bot.handlers.basic_answers import error_message, stop_message, wrong_input_message
from bot.utils.keyboard import EditWalletsKeyboard, WalletsKeyboard
from bot.api.api_requests import WalletAPIRequest
from bot.handlers.handler_config import bot
from bot.schemas.message import MessageNew
from vk_api.utils import get_random_id
import json


wallets_api = WalletAPIRequest()
wallets = {}


def process_new_wallet(message: MessageNew):
    if message.text.lower() in ["стоп", "stop"]:
        stop_message(message)
        return
    _, status = wallets_api.create_new_wallet(message.from_id, message.text)
    if status == 201:
        bot.vk.messages.send(peer_id=message.peer_id,
                             random_id=get_random_id(),
                             message=f"Кошелёк \"{message.text}\" успешно создан!",
                             keyboard=WalletsKeyboard())
    elif status == 401:
        message = "Кошелёк с таким названием уже существует. Придумай что-нибудь другое..."
        bot.vk.messages.send(peer_id=message.peer_id,
                             random_id=get_random_id(),
                             message=message,
                             keyboard=WalletsKeyboard())
    else:
        error_message(message, status)

def edit_choice_step(message: MessageNew):
    if message.payload:
        global wallets
        payload = json.loads(message.payload)    
        wallets[message.from_id] = {"wallet": payload["UUID"]}
        bot.vk.messages.send(peer_id=message.peer_id,
                            random_id=get_random_id(),
                            message="Придумай имя своему кошельку.")
        bot.steps.register_next_step_handler(message.from_id, edit_final_step)
    else:
        wrong_input_message(message)

def edit_final_step(message: MessageNew):
    global wallets
    wallet = wallets.pop(message.from_id)["wallet"]
    _, status = wallets_api.edit_user_wallet(wallet, message.text, message.from_id)
    if status == 200:
        bot.vk.messages.send(peer_id=message.peer_id,
                             random_id=get_random_id(),
                             message=f"Кошелёк `{wallet}` успешно переименован в {message.text}",
                             keyboard=EditWalletsKeyboard())
    else:
        error_message(message, status)

def delete_step(message: MessageNew):
    if message.payload:
        payload = json.loads(message.payload)
        wallet = payload["UUID"]
        status = wallets_api.delete_wallet(wallet)
        if status == 204:
            bot.vk.messages.send(peer_id=message.peer_id,
                                random_id=get_random_id(),
                                message=f"Кошелёк `{wallet}` успешно удалён.",
                                keyboard=EditWalletsKeyboard())
        else:
            error_message(message, status)
    else:
        wrong_input_message(message)
