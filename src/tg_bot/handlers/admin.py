import csv
from io import StringIO, BytesIO
import re

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    Message,
    BufferedInputFile,
)
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from asyncpg import UniqueViolationError

from tg_bot import config
from tg_bot.models.role import UserRole
from tg_bot.states.states import AdminPanel
from tg_bot.lexicon import admin as lex

router = Router()


@router.message(Command(commands="admin"))
async def open_admin_panel(
    message: Message, dialog_manager: DialogManager, role: UserRole
):
    if role == UserRole.ADMIN:
        await dialog_manager.start(AdminPanel.menu, mode=StartMode.RESET_STACK)


async def add_channel(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
):
    """Admin-panel option that allows to add new channel to the database"""
    pattern = r"^https://t\.me/(?P<username>[a-zA-Z0-9_]{5,32})$"
    match = re.match(pattern, message.text)
    if not match:
        await message.answer(lex.WRONG_LINK_FORMAT)
    else:
        # check if bot is admin
        channel = "@" + match.group("username")
        member = await message.bot.get_chat_member(channel, config.BOT_ID)
        if member.status != "administrator":
            await message.answer(lex.BOT_NOT_ADMIN)
        else:
            # define the channel is required to subscription
            checkbox = dialog_manager.find("check_required_channel")
            required = checkbox.is_checked()
            try:
                await dialog_manager.middleware_data["repo"].add_channel(
                    message.text, required
                )
                await message.answer(lex.CHANNEL_ADDED.format(message.text))
            except UniqueViolationError:
                await message.answer(lex.CHANNEL_ALREADY_ADDED)
    await dialog_manager.switch_to(AdminPanel.menu)


async def remove_channel(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
):
    try:
        await dialog_manager.middleware_data["repo"].delete_channel(
            message.text
        )
        await message.answer(lex.CHANNEL_DELETED.format(message.text))
    except ValueError:
        await message.answer(lex.CHANNEL_ALREADY_DELETED)

    await dialog_manager.switch_to(AdminPanel.menu)


async def decide_broadcast(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    """Function that ask the admin for confirmation of the broadcast"""
    if button.widget_id == "confirm_broadcast":
        users = await dialog_manager.middleware_data["repo"].fetch_users_id()
        broadcast_message = dialog_manager.dialog_data["broadcast_message"]
        for user in users:
            await callback.bot.send_message(user, broadcast_message)

        await callback.message.answer(lex.BROADCAST_SUCCESS)

    await dialog_manager.switch_to(AdminPanel.menu)


async def dump_table(
    query: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    """Option that allows to download the table with users data"""
    users = await dialog_manager.middleware_data["repo"].fetch_users_data()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(
        ["Телеграм айди", "Имя пользователя", "Поинты", "Количество рефералов"]
    )
    for user in users:
        writer.writerow(
            [
                user["telegram_id"],
                user["username"],
                user["points"],
                user["referrals_count"],
            ]
        )
    output.seek(0)
    bytes_output = BytesIO(output.read().encode("utf-8"))

    document = BufferedInputFile(bytes_output.read(), "users.csv")
    await query.message.answer_document(
        document=document, caption=lex.CSV_TABLE
    )
    await dialog_manager.switch_to(AdminPanel.menu)
