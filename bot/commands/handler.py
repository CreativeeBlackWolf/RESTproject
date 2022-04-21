from typing import Callable, Dict


class BotCommands:
    def __init__(self) -> None:
        # {"command_text": func}
        self._commands: Dict[str, Callable] = {}

    @property
    def commands(self):
        return self._commands

    def handle(self, text: str):
        def wrapper(func: Callable):
            self._commands.update({text: func})
        return wrapper

    def call_command(self, text, *args, **kwargs):
        try:
            function = self.commands[text]
            function(*args, **kwargs)
        except Exception:
            return
