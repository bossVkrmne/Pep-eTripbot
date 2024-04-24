from aiogram.fsm.state import State, StatesGroup


class MainMenu(StatesGroup):
    menu = State()
    quests = State()


class UserRegistration(StatesGroup):
    check_captcha = State()
    check_subscription = State()
    complete_registration = State()


class AdminPanel(StatesGroup):
    menu = State()
    add_channel = State()
    remove_channel = State()
    start_broadcast = State()
    confirm_broadcast = State()
