# Copyright (c) 2025 iiPython

# Modules
import aiohttp

# Initialization
API_VERSION = "1"

# Connection handling
class Connection:
    def __init__(self, base_url: str) -> None:
        self.client: aiohttp.ClientSession = aiohttp.ClientSession(f"{base_url}/v{API_VERSION}/")

    async def fetch(self, hostname: str, page: str) -> str | None:
        async with self.client.get(f"{hostname}/page/{page}") as response:
            if response.status == 404:
                return None

            return await response.text()

    async def search(self, query: str) -> list[str]:
        async with self.client.post("search", json = {"query": query}) as response:
            return (await response.json())["data"]
