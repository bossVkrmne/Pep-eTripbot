from venv import logger
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput
from aiogram_i18n import I18nContext

from tg_bot.models.reward import Reward
from tg_bot.models.role import UserRole
from tg_bot.services.repository import Repo
from tg_bot.states.states import Config


router = Router()


@router.message(Command(commands="config"))
async def change_config(
    message: Message, dialog_manager: DialogManager, role: UserRole
):
    if role == UserRole.ADMIN:
        await dialog_manager.start(Config.menu, mode=StartMode.RESET_STACK)
    else:
        await dialog_manager.show()


async def remember_attr(
    query: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    dialog_manager.dialog_data["attr"] = button.widget_id
    await dialog_manager.switch_to(Config.change_attr)


async def change_attr(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
):
    repo: Repo = dialog_manager.middleware_data["repo"]
    i18n: I18nContext = dialog_manager.middleware_data["i18n_context"]
    attr = dialog_manager.dialog_data["attr"]
    value = (
        float(message.text) / 100
        if attr == Reward.REFERRER_PART.value
        else float(message.text)
    )
    await repo.change_reward(attr, value)
    await message.answer(i18n.config.reward.changed())
    await dialog_manager.switch_to(Config.menu)
