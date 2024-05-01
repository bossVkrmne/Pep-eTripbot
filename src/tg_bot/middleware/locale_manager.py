from aiogram_dialog import DialogManager
from aiogram_i18n.managers import BaseManager
from aiogram.types import User

from tg_bot.services.repository import Repo


class UserLocaleManager(BaseManager):
    def __init__(self):
        super().__init__()
        self.temp_locale = {}

    async def get_locale(self, event_from_user: User, repo: Repo):
        locale = await repo.get_user_locale(event_from_user.id)
        if not locale:
            try:
                print(self.temp_locale)
                return self.temp_locale[event_from_user.id]
            except KeyError:
                return "en"
        return locale

    async def set_locale(
        self, locale: str, event_from_user: User, repo: Repo, temp: bool
    ):
        if temp:
            self.temp_locale[event_from_user.id] = locale
        else:
            await repo.set_user_locale(event_from_user.id, locale)
