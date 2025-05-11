# Copyright (c) 2025 iiPython

# Modules
import asyncio
from pnv3.client.interface import UI

# Object
class EnterMenu:
    def __init__(self, ui: UI, text: str) -> None:
        self.ui, self.text = ui, text
        self.event = asyncio.Event()

    async def _set(self) -> None:
        self.event.set()

    async def run(self) -> None:
        old_actions = self.ui.get_actions()
        await self.ui.set_actions({"\x11": {"name": "[C+Q] Back", "func": self._set}})

        await self.ui.set_content(self.text)

        async def on_propagate(key: str) -> None:
            if key == "\n":
                self.event.set()

        self.ui.on_propagate(on_propagate)
        await self.event.wait()

        await self.ui.set_actions(old_actions)
        self.ui.remove_propagate(on_propagate)
