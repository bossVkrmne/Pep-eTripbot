import operator

from aiogram import F
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button, Select, Group
from aiogram_dialog.widgets.text import Const, Format

from tg_bot.dialogs.getters import captcha_getter, required_channels_getter
from tg_bot.handlers.auth import process_captcha
from tg_bot.states.states import UserRegistration
from tg_bot.handlers.auth import check_required_subscriptions

captcha_window = Window(
    Format("{text}"),
    Group(
        Select(
            Format("{item[0]}"),
            id="captcha",
            item_id_getter=operator.itemgetter(1),
            on_click=process_captcha,
            items="colors",
        ),
        width=3
    ),
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
