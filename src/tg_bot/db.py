from asyncpg import Pool


async def prepare_db(pool: Pool):
    async with pool.acquire() as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                telegram_id BIGINT UNIQUE,
                username TEXT,
                points FLOAT DEFAULT 10.0,
                ref_code TEXT UNIQUE,
                join_date TIMESTAMPTZ DEFAULT NOW(),
                last_check_in TIMESTAMPTZ DEFAULT NOW() - INTERVAL '1 day'
            );
        """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS referrals (
                referral_id INT,
                referrer_id INT,
                FOREIGN KEY (referral_id) REFERENCES users(user_id),
                FOREIGN KEY (referrer_id) REFERENCES users(user_id)
            );
        """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS channels (
                channel_id SERIAL PRIMARY KEY,
                url TEXT UNIQUE,
                required BOOL
            );            
        """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS user_channels (
            user_id INT,
            channel_id INT,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (channel_id) REFERENCES channels(channel_id) ON DELETE CASCADE
            )
            """
        )
        await db.close()
