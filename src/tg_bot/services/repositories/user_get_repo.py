from datetime import datetime, timedelta, UTC
from typing import Any


class UserGetRepo:
    def __init__(self, db):
        self.db = db

    async def get_by_telegram_id(self, tg_id: int) -> dict[str, Any] | None:
        row = await self.db.fetchrow(
            "SELECT * FROM users WHERE telegram_id = $1", tg_id
        )
        return dict(row) if row else None

    async def get_user_info(self, tg_id: int) -> dict[str, Any] | None:
        row = await self.db.fetchrow(
            """
            SELECT u.telegram_id, u.username, u.points,
            TO_CHAR(u.join_date, 'DD.MM.YYYY') AS join_date, 
            COALESCE(COUNT(r.user_id), 0) AS referral_count

            FROM users u LEFT JOIN referrals r ON u.user_id = r.referrer_id 
            WHERE u.telegram_id = $1 
            GROUP BY u.telegram_id, u.username, u.points, u.join_date
            """,
            tg_id,
        )
        return dict(row) if row else None

    async def get_refcode(self, tg_id: int) -> str | None:
        row = await self.db.fetchrow(
            "SELECT ref_code FROM users WHERE telegram_id = $1", tg_id
        )
        return row["ref_code"] if row else None

    async def get_by_refcode(self, ref_code: str) -> dict[str, Any] | None:
        row = await self.db.fetchrow(
            "SELECT user_id, telegram_id FROM users WHERE ref_code = $1",
            ref_code,
        )
        return dict(row) if row else None

    async def fetch_top_referrers(self) -> list[dict[str, Any]] | None:
        rows = await self.db.fetch(
            """
            SELECT u.username, u.points, COUNT(r.user_id) AS referral_count
            FROM users u
            LEFT JOIN referrals r ON u.user_id = r.referrer_id
            GROUP BY u.user_id
            ORDER BY referral_count DESC, u.points DESC
            LIMIT 10
            """
        )
        return [dict(row) for row in rows]

    async def get_last_check_in(self, tg_id: int) -> datetime:
        row = await self.db.fetchrow(
            "SELECT last_check_in FROM users WHERE telegram_id = $1", tg_id
        )
        if row and row["last_check_in"]:
            return row["last_check_in"].replace(tzinfo=UTC)
        else:
            return datetime.now(UTC) - timedelta(days=1)

    async def fetch_users_id(self) -> list[int]:
        rows = await self.db.fetch("SELECT telegram_id FROM users")
        return [row["telegram_id"] for row in rows]

    async def fetch_users_data(self) -> list[dict[str, Any]]:
        users = await self.db.fetch(
            """
            SELECT u.telegram_id, u.username, u.points,
            COUNT(r.referrer_id) AS referrals_count
            
            FROM users u LEFT JOIN referrals r ON u.user_id = r.referrer_id
            GROUP BY u.user_id
            ORDER BY referrals_count DESC
        """
        )
        return users
