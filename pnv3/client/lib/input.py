# Copyright (c) 2025 iiPython

import asyncio
import logging

from pnv3.client.interface import UI

class InputMenu:
    def __init__(self, ui: UI, prompt: str) -> None:
        self.ui, self.prompt = ui, prompt

        self.value = ""
        self.event = asyncio.Event()

    async def _render(self) -> None:
        await self.ui.set_content(f"{self.prompt}\n  > {self.value}_")

    async def run(self) -> str:
        async def on_propagate(key: str) -> None:
            logging.debug(key.encode())
            match key:
                case "\n":
                    self.event.set()

                case "\x7f":
                    if self.value:  # Can't attach to case, _ will run instead
                        self.value = self.value[:-1]

                case _ if len(key) == 1:
                    self.value += key
                    await self._render()

            await self._render()

        self.ui.on_propagate(on_propagate)

        await self._render()
        await self.event.wait()

        self.ui.remove_propagate(on_propagate)
        return self.value
