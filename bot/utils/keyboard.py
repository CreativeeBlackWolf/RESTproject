from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def MainKeyboard():
    keyboard = VkKeyboard()
    keyboard.add_button(label="Кошельки", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(label="Транзакции", color=VkKeyboardColor.POSITIVE)
    

    return keyboard.get_keyboard()


def WalletsKeyboard():
    keyboard = VkKeyboard()
    keyboard.add_button(label="Создать кошелёк", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(label="Просмотреть кошельки", color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_callback_button(label="Назад", 
                                 payload={"cmd": "back_button"},
                                 color=VkKeyboardColor.NEGATIVE)

    return keyboard.get_keyboard()


def TransactionsKeyBoard():
    keyboard = VkKeyboard()
    keyboard.add_callback_button(label="Просмотреть последние транзакции",
                                 payload={"cmd": "view_latest_transactions"},
                                 color=VkKeyboardColor.PRIMARY)

    keyboard.add_callback_button(label="Назад", 
                                 payload={"cmd": "back_button"},
                                 color=VkKeyboardColor.NEGATIVE)

    return keyboard.get_keyboard()