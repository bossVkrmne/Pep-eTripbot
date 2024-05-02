
class UserUpdateRepo:
    def __init__(self, db):
        self.db = db

    async def update_check_in(self, tg_id: int) -> None:
        await self.db.execute(
            """
            UPDATE users
            SET last_check_in = NOW()
            WHERE telegram_id = $1
            """,
            tg_id,
        )

    async def update_points(self, tg_id: int, points: int) -> None:
        await self.db.execute(
            """
            UPDATE users
            SET points = points + $1
            WHERE telegram_id = $2
            """,
            points, tg_id,
        )