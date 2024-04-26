from datetime import datetime, timedelta
from datetime import UTC

from aiogram import Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from tg_bot.extras import check_subscriptions
from tg_bot.lexicon import core as lex
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
            UserRegistration.check_captcha,
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
    repo = dialog_manager.middleware_data["repo"]
    user_id = query.from_user.id
    last_check_in = await repo.get_last_check_in(user_id)
    next_check_in = last_check_in + timedelta(days=1)

    if datetime.now(UTC) >= last_check_in + timedelta(days=1):
        channels = await repo.fetch_channels()
        subscribed = await check_subscriptions(channels, user_id, query.bot)
        points = len(subscribed)
        if not points:
            await query.message.answer("Вы не подписаны ни на один канал. Подпишитесь, чтобы получить награду!")
            return
        await repo.update_check_in(user_id)
        await repo.update_points(user_id, points)

        referrer_id = await repo.get_user_referrer(user_id)
        if referrer_id and points:
            referrer_points = points * 0.1
            await repo.update_points(referrer_id, referrer_points)

        message = (
            lex.CHECK_IN_REWARD.format(points)
            if points
            else lex.CHECK_IN_NOTHING
        )
    else:
        message = lex.CHECK_IN_OUT.format(
            next_check_in.strftime("%d.%m в %H:%M")
        )
    await query.message.answer(message)


@router.message(Command(commands="info"))
async def info_cmd(message: Message):
    return await message.answer(lex.INFO_TEXT)


@router.message(Command(commands="support"))
async def support_cmd(message: Message):
    return await message.answer(lex.SUPPORT_TEXT)
