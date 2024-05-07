from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput
from aiogram.types import ContentType
from tg_bot.dialogs.getters import config_getter
from tg_bot.handlers.config import remember_attr, change_attr
from tg_bot.i18n.custom_widgets import I18nConst, I18nFormat
from tg_bot.models.reward import Reward
from tg_bot.states.states import Config



config_menu = Window(
    I18nFormat("config-info"),
    Button(
        I18nFormat("button-config-reward-change_checkin"),
        id=Reward.CHECKIN.value,
        on_click=remember_attr
    ),
    Button(
        I18nFormat("button-config-reward-change_subscription"),
        id=Reward.SUBSCRIPTION.value,
        on_click=remember_attr
    ),
    Button(
        I18nFormat("button-config-reward-change_referrer_part"),
        id=Reward.REFERRER_PART.value,
        on_click=remember_attr
    ),
    Button(
        I18nFormat("button-config-reward-change_invitation"),
        id=Reward.INVITATION.value,
        on_click=remember_attr
    ),
    Button(
        I18nFormat("button-config-reward-change_registration"),
        id=Reward.REGISTRATION.value,
        on_click=remember_attr
    ),
    Button(
        I18nFormat("button-config-reward-change_checkin_time"),
        id=Reward.CHECKIN_GAP_HOURS.value,
        on_click=remember_attr
    ),
    state=Config.menu,
    getter=config_getter
)

change_attr = Window(
    I18nConst("config-reward-change_attr"),
    MessageInput(content_types=[ContentType.TEXT], func=change_attr),
    state=Config.change_attr
)

dialog = Dialog(config_menu, change_attr)
