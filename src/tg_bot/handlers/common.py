from typing import Any
from venv import logger
from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext

from tg_bot.states.states import MainMenu, UserRegistration, UserState

router = Router()


async def handle_extra_messages(
    message: Message, widget: Any, dialog_manager: DialogManager
):
    i18n: I18nContext = dialog_manager.middleware_data["i18n_context"]
    await message.answer(i18n.auth.extra_messages())
    return


@router.message(Command(commands="lang"))
async def change_language(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(UserState.change_locale)


async def set_locale(
    query: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    i18n: I18nContext = dialog_manager.middleware_data["i18n_context"]
    try:
        locale = button.widget_id
        await i18n.set_locale(locale, temp=False)
        await query.message.answer(i18n.common.locale_changed())
    except Exception as e:
        logger.error(f"set_locale error: {e}")
    await dialog_manager.done()


@router.message(Command(commands="wallet"))
async def add_wallet(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        UserState.add_wallet, mode=StartMode.RESET_STACK
    )


async def set_wallet(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
):
    i18n = dialog_manager.middleware_data["i18n_context"]
    repo = dialog_manager.middleware_data["repo"]
    wallet_address = message.text
    try:
        await repo.set_wallet(message.from_user.id, wallet_address)
        await message.answer(i18n.common.wallet_added())
    except Exception as e:
        logger.error(f"set_wallet error: {e}")
    await dialog_manager.done()


@router.message(Command(commands="info"))
async def view_info(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(UserState.view_info)


# @router.message(Command(commands="support"))
# async def get_support(message: Message, dialog_manager: DialogManager):
#     i18n = dialog_manager.middleware_data["i18n_context"]
#     await message.answer(i18n.common.support())
