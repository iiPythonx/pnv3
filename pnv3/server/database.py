# Copyright (c) 2025 iiPython

# Modules
from pathlib import Path

import argon2
import secrets
import aiosqlite

# Initialization
DATABASE_LOCATION = Path.cwd() / "data"  # TODO: customize using env variable
if not DATABASE_LOCATION.is_dir():
    DATABASE_LOCATION.mkdir()

# Main object
class Database:
    def __init__(self) -> None:
        self.hasher = argon2.PasswordHasher()
        self.connection: aiosqlite.Connection

    async def init(self) -> None:
        self.connection = await aiosqlite.connect(DATABASE_LOCATION / "users.db")
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS hosts (
                hostname TEXT,
                hash     TEXT,
                token    TEXT
            );
        """)

    async def close(self) -> None:
        await self.connection.close()

    async def validate_token(self, token: str) -> str | None:
        async with self.connection.execute("SELECT hostname FROM hosts WHERE token = ?", (token,)) as response:
            response = await response.fetchone()
            return response[0] if response else None

    async def validate_host(self, hostname: str, password: str) -> str | None:
        async with self.connection.execute("SELECT hash, token FROM hosts WHERE hostname = ?", (hostname,)) as response:
            response = await response.fetchone()
            if response is None:
                return None

            hash, token = response  # type: ignore | once again, pyright is stupid.
            if self.hasher.check_needs_rehash(hash):

                hash = self.hasher.hash(password)
                await self.connection.execute("UPDATE hosts SET hash = ? WHERE token = ?", (hash, token))
                await self.connection.commit()

            try:
                self.hasher.verify(hash, password)
                return token

            except argon2.exceptions.VerificationError:
                return None

    async def register_host(self, hostname: str, password: str) -> tuple[str | None, str | None]:
        async with self.connection.execute("SELECT * FROM hosts WHERE hostname = ?", (hostname,)) as response:
            if await response.fetchone() is not None:
                return None, "The specified hostname is taken."

            token = secrets.token_urlsafe()

            await self.connection.execute("INSERT INTO hosts VALUES (?, ?, ?)", (hostname, self.hasher.hash(password), token))
            await self.connection.commit()
            return token, None

db = Database()
