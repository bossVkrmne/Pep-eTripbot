from datetime import datetime, UTC, timedelta

from aiogram import Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_i18n import I18nContext

from tg_bot import config
from tg_bot.extras import check_subscriptions
from tg_bot.services.repository import Repo
from tg_bot.states.states import UserRegistration, MainMenu

router = Router()


@router.message(CommandStart())
async def start(
    message: Message,
    command: CommandObject,
    dialog_manager: DialogManager,
    repo: Repo,
):
    if await repo.get_by_telegram_id(message.from_user.id):
        return await dialog_manager.start(
            MainMenu.menu, mode=StartMode.RESET_STACK
        )
    else:
        ref = await repo.get_by_refcode(command.args) if command.args else None
        data = {"referrer": ref}
        await dialog_manager.start(
            UserRegistration.select_language,
            data=data,
            mode=StartMode.RESET_STACK,
        )


async def try_check_in(
    query: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    """
    When user checks in, they get points and their referrer too.
    User can check in again in 24h
    """
    i18n = dialog_manager.middleware_data["i18n_context"]
    repo: Repo = dialog_manager.middleware_data["repo"]
    user_id = query.from_user.id
    last_check = await repo.get_last_check_in(user_id)
    next_check = (
        last_check + timedelta(days=1) if last_check else datetime.now(UTC)
    )

    if datetime.now(UTC) >= next_check:
        channels = await repo.fetch_channels()
        subscribed = await check_subscriptions(channels, user_id, query.bot)
        if not subscribed:
            await query.message.answer(i18n.user.check_in.unsub())
            return
        points = len(subscribed) * config.CHECKIN_REWARD
        await repo.update_check_in(user_id)
        await repo.update_points(user_id, points)

        referrer_id = await repo.get_user_referrer(user_id)
        if referrer_id and points:
            await repo.update_points(
                referrer_id, points * config.REFERRER_PART_REWARD
            )

        message = i18n.user.check_in.reward(points=points)
    else:
        message = i18n.user.check_in.unavailable(
            date=next_check.strftime("%H:%M %d.%m")
        )
    await query.message.answer(message)
