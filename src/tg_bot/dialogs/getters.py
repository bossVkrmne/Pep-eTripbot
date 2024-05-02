from aiogram import Bot
from aiogram_dialog import DialogManager
import random
from aiogram.types import User

from tg_bot import config
from tg_bot.services.repository import Repo


async def user_info_getter(repo: Repo, event_from_user: User, **kwargs):
    user_info = await repo.get_user_info(event_from_user.id)
    return {
        "telegram_id": user_info["telegram_id"],
        "username": user_info["username"],
        "points": round(user_info["points"], 2),
        "join_date": user_info["join_date"],
        "referrals": user_info["referral_count"],
    }


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
        ("⬜️", "8"),
    ]
    captcha_key = random.choice(captcha_colors)
    mixed_colors = random.sample(captcha_colors, len(captcha_colors))
    dialog_manager.dialog_data["captcha_key"] = captcha_key[1]

    return {"colors": mixed_colors, "key_color": captcha_key[0]}


async def leaderboard_getter(
    repo: Repo, event_from_user: User, dialog_manager: DialogManager, **kwargs
):
    top_users = await repo.fetch_top_referrers()
    user_rank = await repo.get_user_rank(event_from_user.id)
    top_users_str = (
        f"{index + 1}. {user['username']} - {round(user['points'], 2)} поинтов"
        for index, user in enumerate(top_users)
    )
    top_referrers = "\n".join(top_users_str)
    return {"top_referrers": top_referrers, "user_rank": user_rank}


async def reflink_getter(
    repo: Repo,
    bot: Bot,
    event_from_user: User,
    **kwargs,
):
    refcode = await repo.get_refcode(event_from_user.id)
    bot_obj = await bot.get_me()
    return {"referral_link": f"t.me/{bot_obj.username}?start={refcode}"}


async def newsletter_getter(dialog_manager: DialogManager, **kwargs):
    print(dialog_manager.dialog_data["newsletter_message"])
    return {"newsletter": dialog_manager.dialog_data["newsletter_message"]}


async def required_channels_getter(
    repo: Repo, dialog_manager: DialogManager, **kwargs
):
    channels = await repo.get_required_channels()
    channels = "\n".join(
        f"{index + 1}. {channel}" for index, channel in enumerate(channels)
    )
    unsubscribed = dialog_manager.dialog_data.get("unsubscribed", False)
    return {"channels": channels, "unsubscribed": unsubscribed}


async def wallet_getter(repo: Repo, event_from_user: User, **kwargs):
    wallet = await repo.get_wallet(event_from_user.id)
    return {"wallet": wallet if wallet else None}


async def bot_info_getter(**kwargs):
    return {
        "subscription_reward": config.SUBSCRIPTION_REWARD,
        "checkin_reward": config.CHECKIN_REWARD,
        "invitation_reward": config.INVITATION_REWARD,
        "referrer_part": config.REFERRER_PART_REWARD * 100,
    }


async def quests_info_getter(repo: Repo, **kwargs):
    channels = await repo.get_optional_channels()
    if channels:
        channels = "\n".join(
            f"{index + 1}. {channel}" for index, channel in enumerate(channels)
        )
    return {
        "channels": channels,
        "subscription_reward": config.SUBSCRIPTION_REWARD,
        "checkin_reward": config.CHECKIN_REWARD,
    }
