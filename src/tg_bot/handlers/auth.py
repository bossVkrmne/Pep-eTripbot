from typing import Any
from venv import logger

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram.utils.payload import encode_payload
from aiogram_dialog.widgets.kbd import Button
from aiogram_i18n import I18nContext

from tg_bot import config
from tg_bot.extras import check_subscriptions
from tg_bot.services.repository import Repo
from tg_bot.states.states import UserRegistration, MainMenu, UserState


async def set_locale_registration(
    query: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    i18n: I18nContext = dialog_manager.middleware_data["i18n_context"]
    try:
        locale = button.widget_id
        await i18n.set_locale(locale, temp=True)
    except Exception as e:
        logger.error(f"set_locale_registration error: {e}")
    await dialog_manager.switch_to(UserRegistration.check_captcha)


async def process_captcha(
    query: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
    item_id: str,
):
    if item_id == dialog_manager.dialog_data["captcha_key"]:
        await dialog_manager.switch_to(UserRegistration.check_subscription)
    else:
        dialog_manager.dialog_data["captcha_failed"] = True


async def check_required_subscriptions(
    query: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    i18n: I18nContext = dialog_manager.middleware_data["i18n_context"]
    repo: Repo = dialog_manager.middleware_data["repo"]
    req = await repo.get_required_channels()
    subscribed = await check_subscriptions(req, query.from_user.id, query.bot)
    if len(subscribed) != len(req):
        dialog_manager.dialog_data["unsubscribed"] = True
        return

    await register_user(query, dialog_manager, i18n)


async def check_quest_subscriptions(
    query: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    i18n: I18nContext = dialog_manager.middleware_data["i18n_context"]
    user_id = query.from_user.id
    repo: Repo = dialog_manager.middleware_data["repo"]

    referrer_id = await repo.get_user_referrer(user_id)
    channels = await repo.get_optional_channels()
    user_channels = await repo.get_user_channels(query.from_user.id)
    not_subs = [url for url in channels if url not in user_channels]

    if not not_subs:
        await query.message.answer(i18n.user.quests.already_subscribed())
        return
    try:
        subscribed = await check_subscriptions(not_subs, user_id, query.bot)
        points = len(subscribed) * config.SUBSCRIPTION_REWARD
        if not points:
            await query.message.answer(i18n.user.quests.zero_subsriptions())
            return

        for url in subscribed:
            await repo.add_user_channel(url, query.from_user.id)

        await repo.update_points(query.from_user.id, points)
        await query.message.answer(
            i18n.user.quests.subscription_reward(points=points)
        )
        if referrer_id:
            await repo.update_points(
                referrer_id, points * config.REFERRER_PART_REWARD
            )
    except Exception as e:
        logger.error(f"check_quest_subscriptions error: {e}")
    await dialog_manager.start(MainMenu.menu)


async def register_user(
    query: CallbackQuery, dialog_manager: DialogManager, i18n: I18nContext
):
    repo = dialog_manager.middleware_data["repo"]
    user_id = query.from_user.id
    referrer = dialog_manager.start_data.get("referrer", None)
    locale = i18n.locale
    username = (
        query.from_user.first_name if query.from_user.first_name else "Empty"
    )

    if not referrer:
        try:
            await repo.add_user(
                tg_id=user_id,
                username=username,
                points=config.REGISTRATION_REWARD,
                ref_code=encode_payload(str(user_id)),
                language=locale,
            )
        except Exception as e:
            logger.error(f"register_user single error: {e}")
            await query.message.answer(i18n.error.try_again())
    else:
        try:
            await repo.add_user_referral(
                tg_id=user_id,
                username=username,
                points=config.REGISTRATION_REWARD,
                ref_code=encode_payload(str(user_id)),
                referrer_id=referrer["user_id"],
                referrer_points=config.INVITATION_REWARD,
                language=locale,
            )
            referrer_locale = await repo.get_user_locale(
                referrer["telegram_id"]
            )
            i18n.locale = referrer_locale
            await query.bot.send_message(
                chat_id=referrer["telegram_id"],
                text=i18n.auth.notify_referrer(
                    points=config.INVITATION_REWARD
                ),
            )
            i18n.locale = locale
        except Exception as e:
            logger.error(f"register_user referral error: {e}")
            await query.message.answer(i18n.error.try_again())
    await dialog_manager.start(
        state=UserState.view_info,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )
