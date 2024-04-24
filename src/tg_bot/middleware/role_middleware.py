from typing import Callable, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from black import Any

from tg_bot.models.role import UserRole


class RoleMiddleware(BaseMiddleware):
    def __init__(self, admin_ids: tuple[int]):
        self.admin_ids = admin_ids

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if event.from_user.id in self.admin_ids:
            data["role"] = UserRole.ADMIN
        else:
            data["role"] = UserRole.USER

        print(data["role"])

        return await handler(event, data)
