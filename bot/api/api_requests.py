from typing import Tuple
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError


class APIRequest:
    def __init__(self) -> None:
        self.default_url = "http://web:8000/api/v1"
        self.users_api = self.default_url + "/users/"
        self.session = requests.session()
        self.session.mount("http://", HTTPAdapter(max_retries=5))

    def get_user(self, user_id: int) -> Tuple[dict, int]:
        request = self.session.get(self.users_api + user_id)
        return request.json(), request.status_code

    def get_users(self) -> Tuple[dict, int]:
        request = self.session.get(self.users_api)
        return request.json(), request.status_code

    def create_user(self, user_id: int, name: str) -> Tuple[dict, int]:
        data = {"id": user_id, "user": name}
        request = self.session.post(self.users_api, data = data)
        return request.json(), request.status_code
