from typing import Callable, Dict

from bot.schemas.message import MessageEvent, MessageNew


class BotCommands:
    def __init__(self):
        # {"command_text": func}
        self._commands: Dict[str, Callable] = {}
        self._events: Dict[str, Callable] = {}
        self._default_message_handler: Callable = None


    @property
    def commands(self):
        return self._commands

    @property
    def events(self):
        return self._events

    @property
    def default_message_handler(self):
        """Function that called every time there is no handler for received message"""
        return self._default_message_handler

    @default_message_handler.setter
    def default_message_handler(self, value: Callable):
        if isinstance(value, Callable):
            self._default_message_handler = value
        else:
            raise ValueError(f"Handler must be Callable, not {type(value)}")

    def default_handler(self, func: Callable):
        def wrapper(*args, **kwargs):
            self._default_message_handler = func
        return wrapper

    def handle_command(self, text: str):
        def wrapper(func: Callable):
            self._commands.update({text: func})
        return wrapper

    def handle_event(self, event: str):
        def wrapper(func: Callable):
            self._events.update({event: func})
        return wrapper

    def call_command(self, text, message: MessageNew):
        try:
            function = self.commands[text]
            function(message)
        except KeyError:
            if self.default_message_handler is not None:
                self.default_message_handler(message)

    def call_event(self, event: str, message: MessageEvent):
        try:
            function = self.events[event]
            function(message)
        except KeyError:
            return
