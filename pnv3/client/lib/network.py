# Copyright (c) 2025 iiPython

# Modules
import aiohttp

# Initialization
API_VERSION = "1"

# Connection handling
class Connection:
    def __init__(self, base_url: str) -> None:
        self.base_url = f"{base_url}/v{API_VERSION}"

    async def fetch(self, hostname: str, page: str) -> str | None:
        if self._client is None:
            self._client = aiohttp.ClientSession()

        async with self._client.get(f"/{hostname}/page/{page}") as response:
            if response.status == 404:
                return None

            return await response.text()

    async def search(self, query: str) -> list[str]:
        if self._client is None:
            self._client = aiohttp.ClientSession()

        async with self._client.post("/search", json = {"query": query}) as response:
            return (await response.json())["data"]
