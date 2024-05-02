import operator

from aiogram import F
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button, Select, Group
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Format, Const

from tg_bot.dialogs.getters import captcha_getter, required_channels_getter
from tg_bot.handlers.auth import process_captcha, set_locale_registration
from tg_bot.handlers.common import handle_extra_messages, set_locale
from tg_bot.states.states import UserRegistration
from tg_bot.handlers.auth import check_required_subscriptions

from tg_bot.i18n.custom_widgets import I18nConst, I18nFormat


select_language_window = Window(
    Const("Choose language:"),
    Button(Const("🇷🇺 Русский"), id="ru", on_click=set_locale_registration),
    Button(Const("🇺🇸 English"), id="en", on_click=set_locale_registration),
    MessageInput(func=handle_extra_messages),
    state=UserRegistration.select_language,
)

captcha_window = Window(
    I18nFormat("auth-start_captcha", when=~F["dialog_data"]["captcha_failed"]),
    I18nFormat("auth-failed_captcha", when=F["dialog_data"]["captcha_failed"]),
    Group(
        Select(
            Format("{item[0]}"),
            id="captcha",
            item_id_getter=operator.itemgetter(1),
            on_click=process_captcha,
            items="colors",
        ),
        width=3,
    ),
    MessageInput(func=handle_extra_messages),
    state=UserRegistration.check_captcha,
    getter=captcha_getter,
)

subscribe_window = Window(
    I18nFormat("auth-required_sub-start", when=~F["unsubscribed"]),
    I18nFormat("auth-required_sub-wrong", when=F["unsubscribed"]),
    Button(
        I18nConst("button-common-check_subs"),
        id="check_subscription",
        on_click=check_required_subscriptions,
    ),
    MessageInput(func=handle_extra_messages),
    state=UserRegistration.check_subscription,
    getter=required_channels_getter,
)

dialog = Dialog(select_language_window, captcha_window, subscribe_window)
