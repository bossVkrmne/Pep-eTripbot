from typing import Callable, Dict, Any, Awaitable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject
from asyncpg.pool import Pool

from tg_bot.services.repository import Repo


class DbMiddleware(BaseMiddleware):
    def __init__(self, pool: Pool):
        self.pool = pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        db = await self.pool.acquire()
        try:
            data["repo"] = Repo(db)
            return await handler(event, data)
        finally:
            await db.close()
