from typing import Literal


class UserPostRepo:
    def __init__(self, db):
        self.db = db

    async def add_user(
        self,
        tg_id: int,
        username: str,
        points: int,
        ref_code: str,
        language: Literal["en", "ru"],
    ) -> int:
        user_id = await self.db.fetchval(
            """
            INSERT INTO users
            (telegram_id, username, points, ref_code, language, join_date)
            VALUES ($1, $2, $3, $4, $5, NOW())
            RETURNING user_id
            """,
            tg_id,
            username,
            points,
            ref_code,
            language,
        )
        return user_id

    async def add_user_referral(
        self,
        tg_id: int,
        username: str,
        points: int,
        ref_code: str,
        referrer_id: int,
        referrer_points: int,
        language: Literal["en", "ru"],
    ) -> None:
        async with self.db.transaction():
            user_id = await self.add_user(
                tg_id, username, points, ref_code, language
            )
            await self.db.execute(
                """
                INSERT INTO referrals (referral_id, referrer_id)
                VALUES ($1, $2);
                """,
                user_id,
                referrer_id,
            )
            await self.db.execute(
                """
                UPDATE users
                SET points = points + $1
                WHERE user_id = $2
                """,
                referrer_points,
                referrer_id,
            )
