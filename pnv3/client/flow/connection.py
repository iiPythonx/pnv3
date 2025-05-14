# Copyright (c) 2025 iiPython

# Modules
from pnv3.client.interface import UI
from pnv3.client.lib.network import Connection

# Object
class ConnectionFlow:
    def __init__(self, ui: UI, url: str) -> None:
        self.ui = ui
        self.connection = Connection(url)

    async def run(self) -> None:
        await self.ui.set_content(self.connection.base_url)
