from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Checkbox, Row
from aiogram_dialog.widgets.text import Const

from tg_bot.dialogs.getters import newsletter_getter
from tg_bot.handlers.admin import (
    add_user_points,
    dump_table,
    add_channel,
    remove_channel,
    decide_newsletter,
)
from tg_bot.dialogs.switches import to_newsletter_decide, start_main_menu
from tg_bot.i18n.custom_widgets import I18nConst, I18nFormat
from tg_bot.states.states import Admin

admin_window = Window(
    I18nConst("button-admin-menu"),
    Row(
        SwitchTo(
            I18nConst("button-admin-add_channel"),
            id="add_channel",
            state=Admin.add_channel,
            show_mode=ShowMode.AUTO,
        ),
        SwitchTo(
            I18nConst("button-admin-delete_channel"),
            id="remove_channel",
            state=Admin.remove_channel,
            show_mode=ShowMode.AUTO,
        ),
    ),
    Row(
        SwitchTo(
            I18nConst("button-admin-newsletter"),
            id="broadcast",
            state=Admin.start_newsletter,
            show_mode=ShowMode.AUTO,
        ),
        Button(
            I18nConst("button-admin-dump_table"),
            id="dump_table",
            on_click=dump_table,
        ),
    ),
    SwitchTo(
        I18nConst("button-admin-add_user_points"),
        id="add_user_points",
        state=Admin.add_user_points,
    ),
    Button(
        I18nConst("button-common-back_to_menu"),
        id="back_to_main_menu",
        on_click=start_main_menu,
    ),
    state=Admin.menu,
)

add_channel_window = Window(
    I18nConst("admin-add_channel"),
    MessageInput(content_types=[ContentType.TEXT], func=add_channel),
    Checkbox(
        I18nConst("button-admin-required_channel"),
        I18nConst("button-admin-optional_channel"),
        id="check_required_channel",
        default=False,
    ),
    state=Admin.add_channel,
)

remove_channel_window = Window(
    I18nConst("admin-remove_channel"),
    MessageInput(content_types=[ContentType.TEXT], func=remove_channel),
    state=Admin.remove_channel,
)

start_broadcast_window = Window(
    I18nConst("admin-newsletter"),
    MessageInput(func=to_newsletter_decide),
    state=Admin.start_newsletter,
)

decide_broadcast_window = Window(
    I18nFormat("admin-decide_newsletter"),
    Button(
        I18nConst("button-admin-confirm_newsletter"),
        id="confirm_newsletter",
        on_click=decide_newsletter,
    ),
    Button(
        I18nConst("button-admin-cancel_newsletter"),
        id="cancel_newsletter",
        on_click=decide_newsletter,
    ),
    state=Admin.confirm_newsletter,
    getter=newsletter_getter,
)

add_user_points_window = Window(
    I18nConst("admin-enter_user_points"),
    MessageInput(content_types=[ContentType.TEXT], func=add_user_points),
    state=Admin.add_user_points,
)

dialog = Dialog(
    admin_window,
    add_channel_window,
    remove_channel_window,
    start_broadcast_window,
    decide_broadcast_window,
    add_user_points_window,
)
