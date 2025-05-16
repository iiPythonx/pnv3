# Copyright (c) 2025 iiPython

# Modules

# Connection handling
class Connection:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    async def fetch(self, hostname: str, page: str) -> str | None:
        return None  # TODO

    async def search(self, query: str) -> list[str]:
        return []  # TODO
