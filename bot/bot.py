from typing import Any, Dict, List, Tuple
from vk_api import vk_api
from typing import Optional
from random import choice
from string import ascii_lowercase, ascii_uppercase
from bot.commands.handler import BotCommands


class Bot:
    def __init__(
        self, 
        token: str,
        url: Optional[str] = None,
        group_id: Optional[str] = None,
        secret: Optional[str] = None,
        server_title: Optional[str] = None,
        commands: Optional[BotCommands] = None
    ) -> None:
        self.token = token
        self.api = vk_api.VkApi(token=self.token, api_version="5.131")
        self.vk = self.api.get_api()
        self.url = url
        self.group_id = group_id or self.__get_group_id()
        self.secret = secret or self.__generate_secret_key()
        self.server_title = server_title or "MyCallbackServer"
        self.commands = commands or BotCommands()

    @staticmethod
    def __generate_secret_key() -> str:
        return "".join([choice(ascii_lowercase + ascii_uppercase) for _ in range(32)])

    def __get_group_id(self) -> None:         
        return self.api.method("groups.getById", values={})[0]["id"]

    def get_confirmation_code(self) -> str:
        return self.api.method(
            "groups.getCallbackConfirmationCode", 
            values={
                "group_id": self.group_id
            }
        )["code"]

    def get_callback_servers(self) -> List[Dict[str, Any]]:
        data = {"group_id": self.group_id}
        return self.api.method("groups.getCallbackServers", values=data)["items"]

    def find_server_id(self) -> Optional[int]:
        servers = self.get_callback_servers()

        if not servers:
            return None
        for server in servers:
            if server["url"] == self.url:
                return server["id"]
        return None

    def set_callback_settings(self, server_id: int, params: Dict[str, Any]):
        data = {
            "group_id": self.group_id,
            "server_id": server_id
        }
        data = data | params
        self.api.method("groups.setCallbackSettings", values=data)

    def add_callback_server(self) -> int:
        """
            returns server id
        """
        data = {
            "group_id": self.group_id,
            "secret_key": self.secret,
            "url": self.url,
            "title": self.server_title
        }
        return self.api.method("groups.addCallbackServer", values=data)["id"]

    def edit_callback_server(self, server_id: int, secret_key: Optional[str] = None) -> None:
        if secret_key is None:
            secret_key = self.secret

        data = {
            "group_id": self.group_id,
            "server_id": server_id,
            "url": self.url,
            "title": self.server_title,
            "secret_key": secret_key,
        }
        self.api.method("groups.editCallbackServer", values=data)

    def setup_bot(self) -> Tuple[str, str]:
        """
            returns confirmation code and secret
        """

        confirmation_code: str = self.get_confirmation_code()
        secret: str = self.secret

        server_id = self.find_server_id()

        if server_id is None:
            server_id = self.add_callback_server()
            self.set_callback_settings(server_id, params={
                "message_new": True,
                "message_edit": True,
                "message_event": True
            })
        else:
            self.edit_callback_server(server_id)
        return confirmation_code, secret

    def handle_command(self, data):
        if data["type"] == "message_new":
            self.commands.call_command(data["object"]["message"]["text"], data["object"]["message"])
        elif data["type"] == "message_event":
            self.commands.call_command(data["object"]["payload"]["cmd"], data["object"])
