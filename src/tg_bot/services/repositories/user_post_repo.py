

class UserPostRepo:
    def __init__(self, db):
        self.db = db

    async def add_user(self, tg_id: int, username: str, ref_code: str) -> None:
        await self.db.execute(
            """
            INSERT INTO users
            (telegram_id, username, ref_code, points, join_date)
            VALUES ($1, $2, $3, 10, NOW())
            ON CONFLICT (telegram_id) DO NOTHING
            """,
            tg_id, username, ref_code,
        )

    async def add_referral(
            self,
            tg_id: int,
            username: str,
            ref_code: str,
            refr_id: int,
            refr_points: int = 50,
    ) -> None:
        await self.db.execute(
            """
            WITH ins AS (
                INSERT INTO users
                (telegram_id, username, ref_code, points, join_date)
                VALUES ($1, $2, $3, 10, NOW())
                RETURNING user_id
            )
            INSERT INTO referrals (user_id, referrer_id)
            VALUES ((SELECT user_id FROM ins), $4)
            """,
            tg_id, username, ref_code, refr_id,
        )
        await self.db.execute(
            "UPDATE users SET points = points + $1 WHERE user_id = $2",
            refr_points, refr_id,
        )