from typing import Optional, Tuple, List
from uuid import UUID
import requests
from requests.adapters import HTTPAdapter


class DefaultAPIRequest:
    def __init__(self) -> None:
        self.default_url = "http://web:8000/api/v1/"
        self.session = requests.session()
        self.session.mount("http://", HTTPAdapter(max_retries=5))


class UserAPIRequest(DefaultAPIRequest):
    def __init__(self) -> None:
        super().__init__()
        self.users_url = self.default_url + "users/"

    def get_user(self, user_id: int) -> Tuple[dict, int]:
        request = self.session.get(self.users_url + user_id)
        return request.json(), request.status_code

    def get_users(self) -> Tuple[dict, int]:
        request = self.session.get(self.users_url)
        return request.json(), request.status_code

    def create_user(self, user_id: int, name: str) -> Tuple[dict, int]:
        data = {"id": user_id, "user": name}
        request = self.session.post(self.users_url, data = data)
        return request.json(), request.status_code


class WalletAPIRequest(DefaultAPIRequest):
    def __init__(self) -> None:
        super().__init__()
        self.wallets_url = self.default_url + "wallets/"

    def get_user_wallets(self, user_id: int) -> Tuple[List[dict], int]:
        request = self.session.get(self.wallets_url + f"?user={user_id}")
        return request.json(), request.status_code

    def create_new_wallet(self, user_id: int, wallet_name: str) -> Tuple[dict, int]:
        data = {
            "user": user_id,
            "name": wallet_name
        }
        request = self.session.post(self.wallets_url, data=data)
        return request.json(), request.status_code


class TransactionsAPIRequest(DefaultAPIRequest):
    def __init__(self) -> None:
        super().__init__()
        self.transactions_api = self.default_url + "transactions/"

    def make_transaction(
        self, 
        from_wallet: UUID, 
        payment: int,
        to_wallet: UUID = None, 
        whence: str = None, 
        comment: Optional[str] = None,
        *args, **kwargs
    ) -> Tuple[dict, int]:
        if (to_wallet and whence) or (to_wallet is None and whence is None):
            raise TypeError("One of fields 'from_wallet' or 'whence' must have a value, neither both nor none of them.")
        data = {
            "from_wallet": from_wallet,
            "to_wallet": to_wallet,
            "whence": whence,
            "payment": payment,
            "comment": comment,
        }
        request = self.session.post(self.transactions_api, data=data)
        return request.json(), request.status_code
