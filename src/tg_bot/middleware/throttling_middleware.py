import asyncio
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, TelegramObject


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage, admin_ids: tuple):
        self.storage = storage
        self.admin_ids = admin_ids

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if event.from_user.id in self.admin_ids:
            return await handler(event, data)
        user = f"throttled_{event.from_user.id}"
        value = await self.storage.redis.get(user)
        if value:
            value = int(value.decode())
        else:
            value = 0

        if value == 550:
            return
        elif value == 2:
            await self.storage.redis.set(user, value=550, ex=10)
            msg = "Замечена подозрительная активность. Ждите 10 сек. до ответа"
            if isinstance(event, Message):
                await event.answer(msg)
            else:
                await event.message.answer(msg)
            await asyncio.sleep(10)
            return await handler(event, data)
        else:
            await self.storage.redis.set(user, value=value + 1, ex=1)
            return await handler(event, data)
