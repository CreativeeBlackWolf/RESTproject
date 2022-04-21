from vk_api.keyboard import VkKeyboard, VkKeyboardButton, VkKeyboardColor


def MainKeyboard():
    keyboard = VkKeyboard(inline=False)
    keyboard.add_button(label="Кошельки", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(label="Транзакции", color=VkKeyboardColor.POSITIVE)
    keyboard.add_callback_button(label="test", payload={"cmd": "back_button"})

    return keyboard.get_keyboard()


def WalletsKeyboard():
    keyboard = VkKeyboard(inline=False)
    keyboard.add_button(label="Создать кошелёк", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button(label="Просмотреть кошельки", color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button(label="Назад")

    return keyboard.get_keyboard()