from aiogram import F
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button, SwitchTo
from aiogram_dialog.widgets.text import Format, Const, Multi
from aiogram_dialog import ShowMode

from tg_bot.dialogs.getters import (
    quests_info_getter,
    reflink_getter,
    leaderboard_getter,
    user_info_getter,
)
from tg_bot.handlers.auth import check_quest_subscriptions
from tg_bot.handlers.core import try_check_in
from tg_bot.i18n.custom_widgets import I18nConst, I18nFormat
from tg_bot.states.states import MainMenu

main_menu_window = Window(
    I18nFormat("user-start_info"),
    SwitchTo(
        I18nConst("button-user-ref_link"),
        id="invite_frens",
        state=MainMenu.referral_link,
    ),
    SwitchTo(
        I18nConst("button-user-leadearboard"),
        id="leaderboard",
        state=MainMenu.leaderboard,
    ),
    Button(
        I18nConst("button-user-check_in"), id="check_in", on_click=try_check_in
    ),
    SwitchTo(
        I18nConst("button-user-quests"), id="quests", state=MainMenu.quests
    ),
    state=MainMenu.menu,
    getter=user_info_getter,
)

quests_window = Window(
    I18nFormat("user-quests-info", when=F["channels"]),
    I18nFormat("user-quests-none", when=~F["channels"]),
    Button(
        I18nConst("button-common-check_subs"),
        id="check_subs",
        on_click=check_quest_subscriptions,
        when=F["channels"],
    ),
    SwitchTo(
        I18nConst("button-common-back_to_menu"),
        id="menu",
        state=MainMenu.menu,
    ),
    state=MainMenu.quests,
    getter=quests_info_getter,
)

leadearboard_window = Window(
    Multi(
        I18nFormat("user-leaderboard"),
        I18nFormat("user-user_rank"),
        sep="\n\n",
    ),
    SwitchTo(
        I18nConst("button-common-back_to_menu"), id="menu", state=MainMenu.menu
    ),
    state=MainMenu.leaderboard,
    getter=leaderboard_getter,
)

referral_link_window = Window(
    I18nFormat("user-referral_link"),
    SwitchTo(
        I18nConst("button-common-back_to_menu"), id="menu", state=MainMenu.menu
    ),
    state=MainMenu.referral_link,
    getter=reflink_getter,
)

dialog = Dialog(
    main_menu_window, quests_window, leadearboard_window, referral_link_window
)
