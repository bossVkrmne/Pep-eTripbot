from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Checkbox
from aiogram_dialog.widgets.text import Const, Format

from tg_bot.dialogs.getters import broadcast_message_getter
from tg_bot.handlers.admin import (
    dump_table,
    add_channel,
    remove_channel,
    decide_broadcast,
)
from tg_bot.dialogs.switches import to_broadcast_decide, start_main_menu
from tg_bot.states.states import AdminPanel

admin_window = Window(
    Const("Админ-панель 🚀"),
    SwitchTo(
        Const("Добавить канал ➕"),
        id="add_channel",
        state=AdminPanel.add_channel,
        show_mode=ShowMode.AUTO,
    ),
    SwitchTo(
        Const("Удалить канал ➖"),
        id="remove_channel",
        state=AdminPanel.remove_channel,
        show_mode=ShowMode.AUTO,
    ),
    SwitchTo(
        Const("Рассылка ✍🏻"),
        id="broadcast",
        state=AdminPanel.start_broadcast,
        show_mode=ShowMode.AUTO,
    ),
    Button(Const("Скачать таблицу 📄"), id="dump_table", on_click=dump_table),
    Button(
        Const("⬅️ Вернуться к главному меню"),
        id="back_to_main_menu",
        on_click=start_main_menu,
    ),
    state=AdminPanel.menu,
)

add_channel_window = Window(
    Const("Введите ссылку на канал, который хотите добавить"),
    MessageInput(content_types=[ContentType.TEXT], func=add_channel),
    Checkbox(
        Const("✓ Обязательный канал"),
        Const("✓ Необязательный канал"),
        id="check_required_channel",
        default=False,
    ),
    state=AdminPanel.add_channel,
)

remove_channel_window = Window(
    Const("Введите ссылку на канал, который хотите удалить"),
    MessageInput(content_types=[ContentType.TEXT], func=remove_channel),
    state=AdminPanel.remove_channel,
)

start_broadcast_window = Window(
    Const("Введите сообщение для рассылки"),
    MessageInput(func=to_broadcast_decide),
    state=AdminPanel.start_broadcast,
)

decide_broadcast_window = Window(
    Format(
        'Ваше сообщение для рассылки:\n\n"{broadcast_message}"\n\n'
        "Вы подтверждаете рассылку этого сообщения?"
    ),
    Button(Const("Да"), id="confirm_broadcast", on_click=decide_broadcast),
    Button(Const("Нет"), id="cancel_broadcast", on_click=decide_broadcast),
    state=AdminPanel.confirm_broadcast,
    getter=broadcast_message_getter,
)

dialog = Dialog(
    admin_window,
    add_channel_window,
    remove_channel_window,
    start_broadcast_window,
    decide_broadcast_window,
)
