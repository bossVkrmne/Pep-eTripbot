from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.kbd import Button

from tg_bot.states.states import MainMenu


async def start_main_menu(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    await dialog_manager.start(
        MainMenu.menu, mode=StartMode.RESET_STACK, show_mode=ShowMode.AUTO
    )

