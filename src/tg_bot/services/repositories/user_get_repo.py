from datetime import datetime, timedelta, UTC
from typing import Any


class UserGetRepo:
    def __init__(self, db):
        self.db = db

    async def get_by_telegram_id(self, tg_id: int) -> dict[str, Any] | None:
        user_id = await self.db.fetchval(
            "SELECT user_id FROM users WHERE telegram_id = $1", tg_id
        )
        return user_id

    async def get_user_info(self, tg_id: int) -> dict[str, Any] | None:
        row = await self.db.fetchrow(
            """
            SELECT u.telegram_id, u.username, u.points,
            TO_CHAR(u.join_date, 'DD.MM.YYYY') AS join_date, 
            COALESCE(COUNT(r.referral_id), 0) AS referral_count

            FROM users u LEFT JOIN referrals r ON u.user_id = r.referrer_id 
            WHERE u.telegram_id = $1 
            GROUP BY u.telegram_id, u.username, u.points, u.join_date
            """,
            tg_id,
        )
        return dict(row) if row else None

    async def get_refcode(self, tg_id: int) -> str | None:
        referral_code = await self.db.fetchval(
            "SELECT ref_code FROM users WHERE telegram_id = $1", tg_id
        )
        return referral_code

    async def get_by_refcode(self, ref_code: str) -> dict[str, Any] | None:
        ids = await self.db.fetchrow(
            "SELECT user_id, telegram_id FROM users WHERE ref_code = $1",
            ref_code,
        )
        return dict(ids) if ids else None

    async def fetch_top_referrers(self) -> list[dict[str, Any]] | None:
        referrers = await self.db.fetch(
            """
            SELECT u.username, u.points, COUNT(r.referral_id) AS referral_count
            FROM users u
            LEFT JOIN referrals r ON u.user_id = r.referrer_id
            GROUP BY u.user_id
            ORDER BY u.points DESC
            LIMIT 10
            """
        )
        return referrers

    async def get_user_rank(self, tg_id: int) -> int | None:
        return await self.db.fetchval(
            """
            SELECT rank
            FROM (
                SELECT telegram_id, RANK() OVER (ORDER BY points DESC) AS rank
                FROM users
            ) as ranking
            WHERE telegram_id = $1
            """,
            tg_id,
        )

    async def get_last_check_in(self, tg_id: int) -> datetime:
        last_check_in = await self.db.fetchval(
            "SELECT last_check_in FROM users WHERE telegram_id = $1", tg_id
        )
        print("last ci", last_check_in)
        return last_check_in

    async def fetch_users_id(self) -> list[int]:
        id_rows = await self.db.fetch("SELECT telegram_id FROM users")
        return [row["telegram_id"] for row in id_rows]

    async def fetch_users_data(self) -> list[dict[str, Any]]:
        users = await self.db.fetch(
            """
            SELECT u.telegram_id, u.username, u.points,
            COUNT(r.referrer_id) AS referrals_count, u.wallet
            
            FROM users u LEFT JOIN referrals r ON u.user_id = r.referrer_id
            GROUP BY u.user_id
            ORDER BY referrals_count DESC
        """
        )
        return users

    async def get_user_referrer(self, tg_id: int) -> int | None:
        referrer_id = await self.db.fetchval(
            """
            SELECT u.telegram_id
            FROM users u
            JOIN referrals r ON u.user_id = r.referrer_id
            JOIN users u2 ON r.referral_id = u2.user_id
            WHERE u2.telegram_id = $1
            """,
            tg_id,
        )
        return referrer_id

    async def get_user_locale(self, tg_id: int) -> str | None:
        return await self.db.fetchval(
            "SELECT language FROM users WHERE telegram_id = $1", tg_id
        )

    async def get_wallet(self, tg_id: int) -> str | None:
        return await self.db.fetchval(
            "SELECT wallet FROM users WHERE telegram_id = $1", tg_id
        )
