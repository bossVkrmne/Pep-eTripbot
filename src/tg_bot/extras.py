import io
from typing import Union

from aiogram import Bot
from aiogram.types import (
    BufferedInputFile,
    InputFile, BotCommand
)
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.manager.message_manager import MessageManager
import discapty

from tg_bot import config


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


def draw_captcha(text: str):
    g = discapty.ImageGenerator()
    g.background_color = "#000000"
    g.number_of_curves = 5
    img = g.generate(text)
    out = io.BytesIO()
    img.save(out, format="PNG")
    out.seek(0)
    return out.read()


class CustomMessageManager(MessageManager):
    async def get_media_source(
        self,
        media: MediaAttachment,
        bot: Bot,
    ) -> Union[InputFile, str]:
        if media.file_id:
            return await super().get_media_source(media, bot)
        if media.url and media.url.startswith("bot://"):
            text = media.url[len("bot://") :]
            return BufferedInputFile(draw_captcha(text), f"{text}.png")
        return await super().get_media_source(media, bot)


async def check_subscriptions(channels: list, id: int, bot: Bot):
    subscribed_channels = []
    for channel in channels:
        member = await bot.get_chat_member(
            "@" + channel.split("/")[-1], id
        )
        if member.status != "left":
            subscribed_channels.append(channel)
    return subscribed_channels
