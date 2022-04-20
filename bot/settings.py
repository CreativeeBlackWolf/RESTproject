from pydantic import BaseSettings
from functools import lru_cache


class BotSettings(BaseSettings):
    token: str
    url: str

    class Config:
        env_prefix = "BOT_"
        env_file = ".env"

@lru_cache
def get_bot_settings() -> BotSettings:
    return BotSettings()
