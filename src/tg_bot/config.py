from dataclasses import dataclass
from environs import Env


env: Env = Env()
env.read_env()

BOT_ID: int = env("BOT_ID")
REGISTRATION_REWARD: int = int(env("REGISTRATION_REWARD"))
SUBSCRIPTION_REWARD: int = int(env("REWARD_FOR_SUBSCRIBE"))
CHECKIN_REWARD: int = int(env("CHECKIN_REWARD_FOR_EACH_SUB"))
INVITATION_REWARD: int = int(env("INVITATION_REWARD"))
REFERRER_PART_REWARD: float = float(env("REFERRER_QUANTITY_REWARD"))


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
