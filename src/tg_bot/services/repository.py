from tg_bot.services.repositories.channel_repo import ChannelRepo
from tg_bot.services.repositories.user_get_repo import UserGetRepo
from tg_bot.services.repositories.user_post_repo import UserPostRepo
from tg_bot.services.repositories.user_update_repo import UserUpdateRepo


class Repo(UserGetRepo, UserPostRepo, UserUpdateRepo, ChannelRepo):
    def __init__(self, db):
        super().__init__(db)




