from aiogram import F
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button, SwitchTo
from aiogram_dialog.widgets.text import Format, Const

from tg_bot.dialogs.getters import (
    reflink_getter,
    leaderboard_getter,
    user_info_getter,
    optinonal_channels_getter,
)
from tg_bot.handlers.auth import check_quest_subscriptions
from tg_bot.handlers.core import try_check_in
from tg_bot.states.states import MainMenu

main_menu_window = Window(
    Format("{user_info}"),
    Button(
        Const("Пригласить друзей"), id="invite_frens", on_click=reflink_getter
    ),
    Button(
        Const("Таблица лидеров"), id="leaderboard", on_click=leaderboard_getter
    ),
    Button(Const("Чек-ин"), id="check_in", on_click=try_check_in),
    SwitchTo(Const("Актуальные квесты"), id="quests", state=MainMenu.quests),
    state=MainMenu.menu,
    getter=user_info_getter,
)

quests_window = Window(
    Format("{channels}"),
    Button(
        Const("Проверить подписки"),
        id="check_subs",
        on_click=check_quest_subscriptions,
    ),
    SwitchTo(Const("Вернуться к меню"), id="menu", state=MainMenu.menu),
    state=MainMenu.quests,
    getter=optinonal_channels_getter,
)

dialog = Dialog(main_menu_window, quests_window)
