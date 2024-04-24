from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format

from tg_bot.dialogs.getters import captcha_getter, required_channels_getter
from tg_bot.handlers.auth import process_captcha
from tg_bot.states.states import UserRegistration
from tg_bot.handlers.auth import check_required_subscriptions

captcha_window = Window(
    DynamicMedia("captcha_image"),
    Const("Пройдите капчу для верификации"),
    Button(Const("Обновить капчу"), id="refresh_captcha"),
    MessageInput(content_types=[ContentType.TEXT], func=process_captcha),
    state=UserRegistration.check_captcha,
    getter=captcha_getter,
)

subscribe_window = Window(
    Format("{channels}"),
    Button(
        Const("Проверить подписку ✅"),
        id="check_subscription",
        on_click=check_required_subscriptions,
    ),
    state=UserRegistration.check_subscription,
    getter=required_channels_getter,
)

dialog = Dialog(captcha_window, subscribe_window)
