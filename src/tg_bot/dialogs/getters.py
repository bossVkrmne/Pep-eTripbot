from datetime import date, datetime
from aiogram import Bot
from aiogram_dialog import DialogManager
import random
from aiogram.types import User

from tg_bot.models.reward import Reward
from tg_bot.services.repository import Repo
from tg_bot.config import RAFFLE_START_STR, RAFFLE_START_DATE, RAFFLE_END_STR, RAFFLE_END_DATE


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
    repo: Repo, event_from_user: User, **kwargs
):
    locale = await repo.get_user_locale(event_from_user.id)
    if locale == "ru":
        points = "поинтов"
    else:
        points = "points"
    top_users_dict = await repo.get_top_users()
    user_rank = await repo.get_user_rank(event_from_user.id)
    top_users_collection = (
        f"{index + 1}. {user['username']} - {round(user['points'], 2)} {points}"
        for index, user in enumerate(top_users_dict)
    )
    top_users_str = "\n".join(top_users_collection)
    
    return {
        "top_users": top_users_str,
        "user_rank": user_rank,
        "raffle_not_ended": date.today() <= RAFFLE_END_DATE,
    }


async def raffle_top_getter(
    repo: Repo, event_from_user: User, **kwargs
):
    locale = await repo.get_user_locale(event_from_user.id)
    if locale == "ru":
        referrals = "рефералов"
    else:
        referrals = "referrals"
    top_referrers_dict = await repo.fetch_top_raffle_referrers(
        start_date=RAFFLE_START_DATE, end_date=RAFFLE_END_DATE
    )
    top_referrers_collection = (
        f"{index + 1}. {user['username']} - {user['referrals_count']} {referrals}"
        for index, user in enumerate(top_referrers_dict)
    )
    top_referrers_str = "\n".join(top_referrers_collection)
    return {
        "top_referrers": top_referrers_str,
        "start_date": RAFFLE_START_STR,
        "end_date": RAFFLE_END_STR,
    }



async def reflink_getter(
    repo: Repo,
    bot: Bot,
    event_from_user: User,
    **kwargs,
):
    refcode = await repo.get_refcode(event_from_user.id)
    bot_obj = await bot.get_me()
    return {"referral_link": f"t.me/{bot_obj.username}?start={refcode}"}


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


async def quests_info_getter(repo: Repo, **kwargs):
    channels = await repo.get_optional_channels()
    if channels:
        channels = "\n".join(
            f"{index + 1}. {channel}" for index, channel in enumerate(channels)
        )
    sub_reward = await repo.get_reward_value(Reward.SUBSCRIPTION.value)
    checkin_reward = await repo.get_reward_value(Reward.CHECKIN.value)
    return {
        "channels": channels,
        "subscription_reward": sub_reward,
        "checkin_reward": checkin_reward,
    }


async def users_count_getter(repo: Repo, **kwargs):
    count = await repo.get_users_count()
    return {"count": count}


async def config_getter(repo: Repo, **kwargs):
    rewards = await repo.fetch_rewards()
    result_dict = {}
    for reward in rewards:
        if reward["reward_type"] == Reward.REFERRER_PART.value:
            result_dict[reward["reward_type"]] = reward['value'] * 100
            continue
        result_dict[reward["reward_type"]] = reward["value"]

    return result_dict
