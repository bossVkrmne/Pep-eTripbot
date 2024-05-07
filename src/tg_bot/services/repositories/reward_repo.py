from tg_bot.models.reward import Reward


class RewardRepo:
    def __init__(self, db):
        self.db = db

    async def get_reward_value(self, reward_type: Reward):
        return await self.db.fetchval(
            "SELECT value FROM rewards WHERE reward_type = $1", reward_type
        )

    async def change_reward(self, reward_type: Reward, value: float):
        await self.db.execute(
            "UPDATE rewards SET value = $1 WHERE reward_type = $2",
            value,
            reward_type,
        )

    async def fetch_rewards(self):
        return await self.db.fetch("SELECT * FROM rewards")

