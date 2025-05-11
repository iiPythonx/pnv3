# Copyright (c) 2025 iiPython

# Modules
import string
import typing
import asyncio

from pnv3.client.interface import UI

# Initialization
CHARSET = string.ascii_letters + string.digits + ".:/"

# Object
class InputMenu:
    def __init__(self, ui: UI, prompt: str, footer: typing.Optional[str] = "") -> None:
        self.ui, self.prompt, self.footer = ui, prompt, footer

        self.value = ""
        self.event = asyncio.Event()

    async def _render(self) -> None:
        await self.ui.set_content(f"{self.prompt}\n  > {self.value}_\n\n{self.footer}")

    async def _set(self) -> None:
        self.event.set()

    async def run(self) -> str | None:
        old_actions = self.ui.get_actions()
        await self.ui.set_actions({"\x11": {"name": "[C+Q] Back", "func": self._set}})

        async def on_propagate(key: str) -> None:
            match key:
                case "\n":
                    self.event.set()

                case "\x7f":
                    if self.value:  # Can't attach to case, _ will run instead
                        self.value = self.value[:-1]

                case _ if key in CHARSET:
                    self.value += key
                    await self._render()

            await self._render()

        self.ui.on_propagate(on_propagate)

        await self._render()
        await self.event.wait()

        await self.ui.set_actions(old_actions)
        self.ui.remove_propagate(on_propagate)

        return self.value if self.value.strip() else None
