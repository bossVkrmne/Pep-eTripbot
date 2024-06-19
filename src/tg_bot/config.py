from dataclasses import dataclass
from environs import Env
from datetime import datetime


env: Env = Env()
env.read_env()

BOT_ID = int(env("BOT_ID"))

RAFFLE_START_STR = env("RAFFLE_START")
RAFFLE_END_STR = env("RAFFLE_END")
RAFFLE_START_DATE = datetime.strptime(RAFFLE_START_STR, "%d.%m.%Y").date()
RAFFLE_END_DATE = datetime.strptime(RAFFLE_END_STR, "%d.%m.%Y").date()

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
class RedisConfig:
    host: str
    port: int


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig
    redis: RedisConfig


def load_config():
    return Config(
        tg_bot=TgBot(
            token=env("BOT_TOKEN"),
            admin_ids=tuple(map(int, env("ADMIN_IDS").split(","))),
        ),
        db=DatabaseConfig(
            database=env("DB_NAME"),
            host=env("DB_HOST"),
            port=env("DB_PORT"),
            user=env("DB_USER"),
            password=env("DB_PASSWORD"),
        ),
        redis=RedisConfig(host=env("REDIS_HOST"), port=int(env("REDIS_PORT"))),
    )
