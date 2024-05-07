from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Checkbox, Row
from aiogram_dialog.widgets.text import Const

from tg_bot.dialogs.getters import users_count_getter
from tg_bot.handlers.admin import (
    add_user_points,
    dump_table,
    add_channel,
    remove_channel,
    send_newsletter,
)
from tg_bot.dialogs.switches import start_main_menu
from tg_bot.i18n.custom_widgets import I18nConst, I18nFormat
from tg_bot.states.states import Admin

admin_window = Window(
    I18nFormat("admin-menu"),
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
    getter=users_count_getter,
)

add_channel_window = Window(
    I18nConst("admin-add_channel"),
    MessageInput(content_types=ContentType.ANY, func=add_channel),
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

newsletter_window = Window(
    I18nConst("admin-newsletter"),
    MessageInput(content_types=[ContentType.ANY], func=send_newsletter),
    SwitchTo(
        I18nConst("button-common-back_to_menu"),
        id="back_to_menu",
        state=Admin.menu,
    ),
    state=Admin.start_newsletter,
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
    newsletter_window,
    add_user_points_window,
)
