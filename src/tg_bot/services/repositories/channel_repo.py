class ChannelRepo:
    def __init__(self, db):
        self.db = db

    async def fetch_channels(self) -> list[str]:
        rows = await self.db.fetch("SELECT url FROM channels")
        return [row["url"] for row in rows]

    async def add_channel(self, url: str, required: bool) -> None:
        await self.db.execute(
            "INSERT INTO channels (url, required) VALUES ($1, $2)",
            url,
            required
        )

    async def delete_channel(self, url: str) -> None:
        row = await self.db.fetchrow(
            "SELECT 1 FROM channels WHERE url = $1", url
        )

        if row is None:
            raise ValueError(f"URL '{url}' not found in the database.")

        await self.db.execute("DELETE FROM channels WHERE url = $1", url)

    async def get_required_channels(self) -> list[str]:
        rows = await self.db.fetch(
            "SELECT url FROM channels WHERE required = true"
        )
        return [row["url"] for row in rows]

    async def get_optional_channels(self) -> list[str]:
        rows = await self.db.fetch(
            "SELECT url FROM channels WHERE required = false"
        )
        return [row["url"] for row in rows]

    async def get_user_channels(self, tg_id: int) -> list[str]:
        rows = await self.db.fetch(
            """
            SELECT c.url
            FROM users u
            JOIN user_channels uc ON u.user_id = uc.user_id
            JOIN channels c ON uc.channel_id = c.channel_id
            WHERE u.telegram_id = $1;
            """,
            tg_id,
        )
        return [row["url"] for row in rows]

    async def add_user_channel(self, url: str, tg_id: int) -> None:
        user_id = await self.db.fetchval(
            "SELECT user_id FROM users WHERE telegram_id = $1", tg_id,
        )

        channel_id = await self.db.fetchval(
            "SELECT channel_id FROM channels WHERE url = $1", url,
        )

        await self.db.execute(
            """
            INSERT INTO user_channels (user_id, channel_id)
            VALUES ($1, $2)
            """,
            user_id, channel_id,
        )
