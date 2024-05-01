from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from tg_bot.states.states import MainMenu, AdminPanel


async def start_main_menu(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    await dialog_manager.start(
        MainMenu.menu, mode=StartMode.RESET_STACK, show_mode=ShowMode.AUTO
    )


async def to_newsletter_decide(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
):
    dialog_manager.dialog_data["newsletter_message"] = message.text
    await dialog_manager.switch_to(AdminPanel.confirm_newsletter)
