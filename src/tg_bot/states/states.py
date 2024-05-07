from aiogram.fsm.state import State, StatesGroup


class MainMenu(StatesGroup):
    menu = State()
    quests = State()
    leaderboard = State()
    referral_link = State()


class UserState(StatesGroup):
    change_locale = State()
    add_wallet = State()
    view_info = State()


class UserRegistration(StatesGroup):
    select_language = State()
    check_captcha = State()
    check_subscription = State()
    complete_registration = State()


class Admin(StatesGroup):
    menu = State()
    add_channel = State()
    remove_channel = State()
    start_newsletter = State()
    confirm_newsletter = State()
    add_user_points = State()


class Config(StatesGroup):
    menu = State()
    change_attr = State()
