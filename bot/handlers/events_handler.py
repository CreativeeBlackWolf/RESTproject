from bot.utils.keyboard import MainKeyboard, WalletsKeyboard, TransactionsKeyboard
from bot.utils.redis_utils import is_registered_user, add_new_users
from bot.handlers.handler_config import bot
from bot.schemas.message import MessageEvent
from bot.api.api_requests import UserAPIRequest, WalletAPIRequest


user_api = UserAPIRequest()
wallet_api = WalletAPIRequest()


@bot.commands.handle_event(event="back_button")
def back_button_event(event: MessageEvent):
    is_registered: bool = is_registered_user(event.user_id)
    bot.vk.messages.send(peer_id=event.peer_id,
                         random_id=0,
                         message="Возвращаемся в главное меню",
                         keyboard=MainKeyboard(is_registered))


@bot.commands.handle_event(event="register_user")
def register_user_event(event: MessageEvent):
    user = bot.vk.users.get(user_ids=event.user_id)[0]
    _, status = user_api.create_user(event.user_id, user["first_name"] + " " + user["last_name"])
    if status == 201:
        add_new_users(str(event.user_id))
        bot.vk.messages.send(peer_id=event.peer_id,
                             random_id=0,
                             message="Ты успешно зарегистрировался!",
                             keyboard=MainKeyboard(True))
    else:
        bot.vk.messages.send(peer_id=event.peer_id,
                             random_id=0,
                             message=f"Что-то пошло не так... ({status}). Сообщи об этом.",
                             keyboard=MainKeyboard())


@bot.commands.handle_event(event="user_wallets")
def get_user_wallets(event: MessageEvent):
    wallets, status = wallet_api.get_user_wallets(event.user_id)
    if status == 200:
        if not wallets:
            bot.vk.messages.send(peer_id=event.peer_id,
                                 random_id=0,
                                 message="Пока что у тебя нет кошельков.",
                                 keyboard=WalletsKeyboard())
        else:
            message = "Твои кошельки:\n\n"
            for k, wallet in enumerate(wallets):
                message += \
f"""
{k+1}) Уникальный идентификатор: {wallet["pk"]}
| Название: {wallet["name"]}
| Баланс: {wallet["balance"]}
"""
            bot.vk.messages.send(peer_id=event.peer_id,
                                 random_id=0,
                                 message=message,
                                 keyboard=WalletsKeyboard())
    else:
        bot.vk.messages.send(peer_id=event.peer_id,
                             random_id=0,
                             message=f"Что-то пошло не так... ({status}). Сообщи об этом.",
                             keyboard=MainKeyboard())