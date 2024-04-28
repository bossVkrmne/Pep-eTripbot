from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram.utils.payload import encode_payload
from aiogram_dialog.widgets.kbd import Button

from tg_bot import config
from tg_bot.extras import check_subscriptions
from tg_bot.lexicon import auth as lex
from tg_bot.states.states import UserRegistration, MainMenu


async def process_captcha(
    query: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
    item_id: str,
):
    print(type(item_id), type(dialog_manager.dialog_data["captcha_key"]))
    if item_id == dialog_manager.dialog_data["captcha_key"]:
        await dialog_manager.switch_to(UserRegistration.check_subscription)
    else:
        dialog_manager.dialog_data["captcha_failed"] = True


async def check_required_subscriptions(
    query: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    """Check if all required channels are subscribed on registration"""
    req = await dialog_manager.middleware_data["repo"].get_required_channels()
    subscribed = await check_subscriptions(req, query.from_user.id, query.bot)
    if len(subscribed) != len(req):
        return await query.message.answer(lex.NOT_SUBSCRIBED)

    state = dialog_manager.middleware_data["state"]
    await state.set_state(UserRegistration.complete_registration)
    await register_user(query, dialog_manager)


async def check_quest_subscriptions(
    query: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    """Check optional subscriptions and reward the user"""
    user_id = query.from_user.id
    repo = dialog_manager.middleware_data["repo"]
    channels = await repo.get_optional_channels()
    user_channels = await repo.get_user_channels(query.from_user.id)

    not_subs = [url for url in channels if url not in user_channels]
    if not not_subs:
        return await query.message.answer(lex.ALREADY_SUBSCRIBED)
    else:
        subscribed = await check_subscriptions(not_subs, user_id, query.bot)
        points = len(subscribed)

        for url in subscribed:
            await repo.add_user_channel(url, query.from_user.id)

        total = points * config.SUBSCRIBE_POINTS_MULTIPLIER
        await repo.update_points(query.from_user.id, total)
        await query.message.answer(lex.SUBSCRIBE_REWARD.format(total, points))
    await dialog_manager.start(MainMenu.menu)


async def register_user(query: CallbackQuery, dialog_manager: DialogManager):
    """Register the user in the database"""
    repo = dialog_manager.middleware_data["repo"]
    user_id = query.from_user.id
    referrer = dialog_manager.start_data.get("referrer", None)

    if not referrer:
        await repo.add_user(
            tg_id=user_id,
            username=query.from_user.username,
            points=config.DEFAULT_REGISTRATION_POINTS,
            ref_code=encode_payload(str(user_id)),
        )
    else:
        await repo.add_user_referral(
            tg_id=user_id,
            username=query.from_user.username,
            points=config.DEFAULT_REGISTRATION_POINTS,
            ref_code=encode_payload(str(user_id)),
            referrer_id=referrer["user_id"],
            referrer_points=config.INVITATION_REWARD,
        )
        await query.bot.send_message(
            referrer["telegram_id"],
            lex.NOTIFY_REFERRER_REG.format(config.INVITATION_REWARD),
        )
    await dialog_manager.start(
        MainMenu.menu, mode=StartMode.RESET_STACK, show_mode=ShowMode.SEND
    )
