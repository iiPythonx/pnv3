# Copyright (c) 2025 iiPython

# Modules
import typing
import asyncio

from pnv3.client.interface import UI

# Object
class SelectMenu:
    def __init__(self, ui: UI, prompt: str, options: list[str], footer: typing.Optional[str] = "") -> None:
        self.ui, self.prompt, self.options, self.footer = ui, prompt, options, footer

        self.index = 0
        self.event = asyncio.Event()

    async def _render(self) -> None:
        content = self.prompt
        for index, option in enumerate(self.options):
            content += f"\n  {'\033[32m●' if index == self.index else '○'} {option}\033[0m"

        await self.ui.set_content(f"{content}\n\n{self.footer}")

    async def run(self) -> str:
        async def on_propagate(key: str) -> None:
            match key:
                case "UP" if self.index:
                    self.index -= 1

                case "DN" if self.index < len(self.options) - 1:
                    self.index += 1

                case "\n":
                    self.event.set()

            await self._render()

        self.ui.on_propagate(on_propagate)

        await self._render()
        await self.event.wait()

        self.ui.remove_propagate(on_propagate)
        return self.options[self.index]
