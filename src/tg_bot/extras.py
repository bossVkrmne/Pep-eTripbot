from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot) -> None:
    main_menu_commands = [
        BotCommand(command="/start", description="Открыть основное меню"),
        BotCommand(
            command="/info",
            description="Ознакомительная информация о боте",
        ),
        BotCommand(
            command="/support",
            description="Если вы столкнулись с ошибками/багами - тыкайте сюда",
        ),
    ]

    await bot.set_my_commands(main_menu_commands)


async def check_subscriptions(channels: list, tg_id: int, bot: Bot):
    subscribed_channels = []
    for channel in channels:
        member = await bot.get_chat_member("@" + channel.split("/")[-1], tg_id)
        if member.status != "left":
            subscribed_channels.append(channel)
    return subscribed_channels
