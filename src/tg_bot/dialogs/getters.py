from aiogram_dialog import DialogManager
import random
from aiogram.types import CallbackQuery

from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.kbd import Button
import string
from aiogram.enums import ContentType

from tg_bot.lexicon import getters as lex
from tg_bot.services.repository import Repo


async def user_info_getter(
    repo: Repo, dialog_manager: DialogManager, **kwargs
):
    user_info = await repo.get_user_info(dialog_manager.event.from_user.id)
    response_msg = lex.USER_INFO.format(**user_info)
    return {"user_info": response_msg}


async def captcha_getter(dialog_manager: DialogManager, **kwargs):
    captcha_colors = [
        ("🟥", "0"),
        ("🟧", "1"),
        ("🟨", "2"),
        ("🟩", "3"),
        ("🟦", "4"),
        ("🟪", "5"),
        ("🟫", "6"),
        ("⬛️", "7"),
        ("⬜️", "8")
    ]
    captcha_key = random.choice(captcha_colors)
    mixed_colors = random.sample(captcha_colors, len(captcha_colors))
    dialog_manager.dialog_data["captcha_key"] = captcha_key[1]

    if dialog_manager.dialog_data.get("captcha_failed", False):
        msg = lex.CAPTCHA_FAILED.format(captcha_key[0])
    else:
        msg = lex.CAPTCHA_START.format(captcha_key[0])
    return {"colors": mixed_colors, "text": msg}



async def leaderboard_getter(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    top = await dialog_manager.middleware_data["repo"].fetch_top_referrers()
    if not top:
        await callback.answer()
        return await callback.message.answer(lex.NO_REFERRERS)

    referrers = (
        f"{index + 1}. {referrer['username']} - {referrer['points']} поинтов"
        for index, referrer in enumerate(top)
    )
    response_message = "🏆 Топ рефереров 🏆\n\n" + "\n".join(referrers)

    return await callback.message.answer(response_message)


async def reflink_getter(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    refcode = await dialog_manager.middleware_data["repo"].get_refcode(
        callback.from_user.id
    )
    return await callback.message.answer(lex.REF_LINK.format(refcode))


async def broadcast_message_getter(dialog_manager: DialogManager, **kwargs):
    return {
        "broadcast_message": dialog_manager.dialog_data["broadcast_message"]
    }


async def optinonal_channels_getter(repo: Repo, **kwargs):
    channels = await repo.get_optional_channels()
    if not channels:
        response_msg = lex.IF_NOT_OPTINAL_CHANNELS
    else:
        channels_str = "\n".join(
            f"{index + 1}. {channel}" for index, channel in enumerate(channels)
        )
        response_msg = lex.IF_OPTIONAL_CHANNELS.format(channels_str)
    return {"channels": response_msg}


async def required_channels_getter(repo: Repo, **kwargs):
    channels = await repo.get_required_channels()
    channels_response = "\n".join(
        f"{index + 1}. {channel}" for index, channel in enumerate(channels)
    )
    response_msg = lex.REQUIRE_SUBSCRIBE_MESSAGE.format(channels_response)
    return {"channels": response_msg}
