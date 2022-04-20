from vkbottle import Keyboard, KeyboardButtonColor, Text

BASE_KEYBOARD = (
    Keyboard(one_time=True, inline=False)
    .add(Text("Button 1"), color=KeyboardButtonColor.POSITIVE)
    .add(Text("Button 2"))
    .row()
    .add(Text("Button 3"))
    .get_json()
)

