from dataclasses import dataclass
from environs import Env

SUBSCRIBE_POINTS_MULTIPLIER: int = 10
CHECK_IN_POINTS_MULTIPLIER: int = 1
INVITATION_REWARD: int = 50


@dataclass
class DatabaseConfig:
    database: str
    host: str
    port: str
    user: str
    password: str


@dataclass
class TgBot:
    token: str
    admin_ids: tuple


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


env: Env = Env()
env.read_env()

BOT_ID: int = env("BOT_ID")


def load_config():
    return Config(
        tg_bot=TgBot(
            token=env("BOT_TOKEN"),
            admin_ids=tuple(map(int, env("ADMIN_IDS").split(",")))
        ),
        db=DatabaseConfig(
            database=env("DB_NAME"),
            host=env("DB_HOST"),
            port=env("DB_PORT"),
            user=env("DB_USER"),
            password=env("DB_PASSWORD"),
        ),
    )
