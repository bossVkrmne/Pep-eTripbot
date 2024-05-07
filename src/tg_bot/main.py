import asyncio
import logging

from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore
import asyncpg
from asyncpg import Pool

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis, DefaultKeyBuilder
from aiogram.exceptions import TelegramAPIError

from tg_bot.config import load_config
from tg_bot.db import prepare_db
from tg_bot.extras import set_main_menu

from tg_bot.dialogs.core import dialog as core
from tg_bot.dialogs.auth import dialog as auth
from tg_bot.dialogs.admin import dialog as admin
from tg_bot.dialogs.common import dialog as common
from tg_bot.dialogs.config import dialog as config_dialog

from tg_bot.handlers.core import router as core_router
from tg_bot.handlers.admin import router as admin_router
from tg_bot.handlers.common import router as common_router
from tg_bot.handlers.config import router as config_router

from tg_bot.middleware.db_middleware import DbMiddleware
from aiogram_dialog import setup_dialogs

from tg_bot.middleware.locale_manager import UserLocaleManager
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
        filename="Logs/logs.log",
    )
    logger.error("Starting bot")
    config = load_config()

    redis = Redis(host=config.redis.host, port=config.redis.port)
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

    i18n_middleware = I18nMiddleware(
        core=FluentRuntimeCore("./src/tg_bot/i18n/locales"),
        context_key="i18n_context",
        manager=UserLocaleManager(),
    )
    dp.update.outer_middleware(DbMiddleware(pool))
    admin_router.message.middleware(RoleMiddleware(config.tg_bot.admin_ids))
    config_router.message.middleware(RoleMiddleware(config.tg_bot.admin_ids))

    throttling_middleware = ThrottlingMiddleware(
        storage, config.tg_bot.admin_ids
    )
    dp.message.middleware(throttling_middleware)
    dp.callback_query.middleware(throttling_middleware)
    i18n_middleware.setup(dp)

    dp.startup.register(set_main_menu)

    dp.include_routers(
        core_router,
        auth.dialog,
        admin_router,
        common_router,
        config_router,
        core.dialog,
        admin.dialog,
        common.dialog,
        config_dialog.dialog,
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
    except (KeyboardInterrupt, SystemExit, TelegramAPIError):
        logger.error("Bot stopped!")


if __name__ == "__main__":
    cli()
