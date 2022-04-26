from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def EmptyKeyboard():
    return VkKeyboard.get_empty_keyboard()

def MainKeyboard(registered_user: bool = False):
    keyboard = VkKeyboard()
    keyboard.add_button(label="Кошельки", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(label="Транзакции", color=VkKeyboardColor.POSITIVE)
    
    if not registered_user:
        keyboard.add_line()
        keyboard.add_callback_button(label="Зарегистрироваться", 
                                     payload={"cmd": "register_user"},
                                     color=VkKeyboardColor.NEGATIVE)

    return keyboard.get_keyboard()

def WalletsKeyboard():
    keyboard = VkKeyboard()
    keyboard.add_callback_button(label="Создать кошелёк", 
                                 color=VkKeyboardColor.PRIMARY,
                                 payload={
                                     "cmd": "create_wallet"
                                 })
    keyboard.add_callback_button(label="Просмотреть кошельки", 
                                 color=VkKeyboardColor.SECONDARY,
                                 payload={"cmd": "user_wallets"})
    keyboard.add_line()
    keyboard.add_callback_button(label="Назад", 
                                 payload={"cmd": "back_button"},
                                 color=VkKeyboardColor.NEGATIVE)

    return keyboard.get_keyboard()

def TransactionsKeyboard():
    keyboard = VkKeyboard()
    keyboard.add_callback_button(label="Просмотреть последние транзакции",
                                 payload={"cmd": "view_latest_transactions"},
                                 color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_callback_button(label="Перевести деньги",
                                 payload={"cmd": "make_transaction"},
                                 color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_callback_button(label="Назад", 
                                 payload={"cmd": "back_button"},
                                 color=VkKeyboardColor.NEGATIVE)

    return keyboard.get_keyboard()

def UserWalletsKeyboard(wallets: list):
    keyboard = VkKeyboard(one_time=True)
    for wallet in wallets:
        keyboard.add_button(label=f"{wallet['name']} | Баланс: {wallet['balance']}",
                            color=VkKeyboardColor.POSITIVE,
                            payload={"UUID": wallet["pk"]})
    return keyboard.get_keyboard()
