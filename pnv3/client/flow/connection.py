# Copyright (c) 2025 iiPython

# Modules
from pnv3.client.interface import UI
from pnv3.client.lib.xtract import parse
from pnv3.client.lib.network import Connection

# Object
class ConnectionFlow:
    def __init__(self, ui: UI, url: str) -> None:
        self.ui = ui
        self.connection = Connection(url)

    async def fetch_page(self, url: str) -> None:
        content = await self.connection.fetch(*url.split("::"))
        if content is None:
            return await self.ui.set_content("The specified URL does not exist.")

        title, content = parse(content)
        await self.ui.set_content(content)

    async def run(self) -> None:
        await self.fetch_page("iipython::index")
