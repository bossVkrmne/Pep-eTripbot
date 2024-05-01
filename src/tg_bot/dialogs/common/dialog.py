from aiogram import F
from aiogram.types import ContentType
from tg_bot.dialogs.getters import bot_info_getter, wallet_getter
from tg_bot.dialogs.switches import start_main_menu
from tg_bot.handlers.common import set_locale, set_wallet
from tg_bot.i18n.custom_widgets import I18nConst, I18nFormat
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Multi
from aiogram_dialog.widgets.input import MessageInput

from tg_bot.states.states import UserState


change_locale_window = Window(
    I18nConst("common-change_language"),
    Button(Const("🇷🇺 Русский"), id="ru", on_click=set_locale),
    Button(Const("🇺🇸 English"), id="en", on_click=set_locale),
    state=UserState.change_locale,
)

info_window = Window(
    I18nFormat("common-info"),
    Button(
        I18nConst("button-common-start_menu"),
        id="back_to_menu",
        on_click=start_main_menu,
    ),
    state=UserState.view_info,
    getter=bot_info_getter,
)

add_wallet_window = Window(
    Multi(
        I18nFormat("common-show_wallet", when=F["wallet"]),
        I18nConst("common-show_wallet_none", when=~F["wallet"]),
        I18nConst("common-wallet_info"),
        I18nConst("common-add_new_wallet", when=~F["wallet"]),
        I18nConst("common-replace_wallet", when=F["wallet"]),
        sep="\n\n",
    ),
    MessageInput(content_types=[ContentType.TEXT], func=set_wallet),
    Button(
        I18nConst("button-common-back_to_menu"),
        id="back_to_menu",
        on_click=start_main_menu,
    ),
    state=UserState.add_wallet,
    getter=wallet_getter,
)

dialog = Dialog(change_locale_window, add_wallet_window, info_window)
