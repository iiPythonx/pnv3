# Copyright (c) 2025 iiPython

# Modules
import re
from pathlib import Path

import argon2
import secrets
import aiosqlite

# Initialization
DATABASE_LOCATION = Path.cwd() / "data"  # TODO: customize using env variable
if not DATABASE_LOCATION.is_dir():
    DATABASE_LOCATION.mkdir()

FILE_LOCATION = DATABASE_LOCATION / "pages"
if not FILE_LOCATION.is_dir():
    FILE_LOCATION.mkdir()

# Regex handling
HOSTNAME_REGEX = re.compile(r"\w{3,16}")
PASSWORD_REGEX = re.compile(r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{12,}")
PAGENAME_REGEX = re.compile(r"\w{1,20}\.html")

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
            )
        """)
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS pages (
                host TEXT,
                page TEXT
            )
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
        if HOSTNAME_REGEX.match(hostname) is None:
            return None, "Hostname must be 3-16 characters of alphanumerics, including _."

        if PASSWORD_REGEX.match(password) is None:
            return None, "Password does not meet complexity requirements."

        async with self.connection.execute("SELECT * FROM hosts WHERE hostname = ?", (hostname,)) as response:
            if await response.fetchone() is not None:
                return None, "The specified hostname is taken."

            token = secrets.token_urlsafe()

            await self.connection.execute("INSERT INTO hosts VALUES (?, ?, ?)", (hostname, self.hasher.hash(password), token))
            await self.create_page(hostname, "index.html")

            await self.connection.commit()
            return token, None

    # Handle pages
    async def fetch_pages(self, hostname: str) -> tuple[str] | None:
        async with self.connection.execute("SELECT * FROM hosts WHERE hostname = ?", (hostname,)) as response:
            if await response.fetchone() is None:
                return None

        async with self.connection.execute("SELECT page FROM pages WHERE host = ?", (hostname,)) as response:
            return [item[0] for item in await response.fetchall()]  # type: ignore

    def fetch_page(self, hostname: str, page: str) -> bytes | None:
        page_file = FILE_LOCATION / hostname / f"{page.removesuffix('.html')}.html"
        if not (page_file.is_file() and page_file.is_relative_to(FILE_LOCATION / hostname)):
            return None

        # I eventually intend on supporting things OTHER then text.
        return page_file.read_bytes()

    async def create_page(self, hostname: str, page: str) -> str | None:
        if not PAGENAME_REGEX.match(page):
            return "Specified filename is invalid."

        # Handle file IO
        page_file = FILE_LOCATION / hostname / page
        if page_file.is_file() or not page_file.is_relative_to(FILE_LOCATION / hostname):
            return "Specified filename is already in use."

        page_file.parent.mkdir(exist_ok = True)
        page_file.write_text("<title></title>\n<body>\n</body>")

        # Add to database
        await self.connection.execute("INSERT INTO pages VALUES (?, ?)", (hostname, page.removesuffix(".html")))
        await self.connection.commit()

        return None

    async def delete_page(self, hostname: str, page: str) -> str | None:
        page_file = FILE_LOCATION / hostname / page
        if not page_file.is_file() or not page_file.is_relative_to(FILE_LOCATION / hostname):
            return "Specified file does not exist on this server."

        # Remove from database
        await self.connection.execute("DELETE FROM pages WHERE host = ? AND page = ?", (hostname, page.removesuffix(".html")))
        await self.connection.commit()

        return page_file.unlink()

    def write_page(self, hostname: str, filename: str, content: str) -> str | None:
        page_file = FILE_LOCATION / hostname / filename
        if not page_file.is_file() or not page_file.is_relative_to(FILE_LOCATION / hostname):
            return "Specified file does not exist on this server."

        page_file.write_text(content)
        return None

    async def search_pages(self, query: str) -> list[str]:
        async with self.connection.execute("SELECT host, page FROM pages WHERE host LIKE ? OR page LIKE ?", (f"%{query}%",) * 2) as response:
            return ["::".join(item) for item in await response.fetchall()]

db = Database()
