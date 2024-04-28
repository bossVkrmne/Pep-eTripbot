import asyncio
import logging

import asyncpg
from asyncpg import Pool

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis, DefaultKeyBuilder

from tg_bot.config import load_config
from tg_bot.db import prepare_db
from tg_bot.extras import set_main_menu
from tg_bot.dialogs.core import dialog as core
from tg_bot.dialogs.auth import dialog as auth
from tg_bot.dialogs.admin import dialog as admin
from tg_bot.handlers.core import router as core_router
from tg_bot.handlers.admin import router as admin_router
from tg_bot.middleware.db_middleware import DbMiddleware

from aiogram_dialog import setup_dialogs

from tg_bot.middleware.role_middleware import RoleMiddleware
from tg_bot.middleware.throttling_middleware import ThrottlingMiddleware

logger = logging.getLogger(__name__)


async def create_pool(user, password, host, port, database) -> Pool:
    dsn = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    return await asyncpg.create_pool(dsn=dsn)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    config = load_config()

    redis = Redis(host="localhost", port=6379)
    storage = RedisStorage(redis, DefaultKeyBuilder(with_destiny=True))

    pool = await create_pool(
        user=config.db.user,
        password=config.db.password,
        host=config.db.host,
        port=config.db.port,
        database=config.db.database,
    )
    await prepare_db(pool)

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(storage=storage)

    dp.update.middleware(DbMiddleware(pool))
    admin_router.message.middleware(RoleMiddleware(config.tg_bot.admin_ids))
    throttling_middleware = ThrottlingMiddleware(storage)
    dp.message.middleware(throttling_middleware)
    dp.callback_query.middleware(throttling_middleware)

    dp.startup.register(set_main_menu)
    dp.include_routers(
        core_router, admin_router, auth.dialog, core.dialog, admin.dialog
    )
    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()


def cli():
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")


if __name__ == "__main__":
    cli()
