from dataclasses import dataclass
from environs import Env


env: Env = Env()
env.read_env()

BOT_ID: int = int(env("BOT_ID"))

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
