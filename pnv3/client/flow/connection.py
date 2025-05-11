# Copyright (c) 2025 iiPython

# Modules
import typing
from urllib.parse import urlparse

from pnv3.client import xlen
from pnv3.client.interface import UI
from pnv3.client.objects import InputMenu, SelectMenu, EnterMenu

# Object
class ConnectionFlow:
    def __init__(self, ui: UI) -> None:
        self.ui = ui

    @staticmethod
    def prompt(text: str, footer: str) -> dict[str, str]:
        return {
            "prompt": text,
            "footer": f"{'─' * xlen(footer)}\n{footer}"
        }

    @staticmethod
    def normalize(url: str) -> tuple[bool, str]:
        if "://" not in url:
            url = "https://" + url

        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False, "Protocol must be either HTTP or HTTPS!"

        if not parsed.netloc:
            return False, "No valid domain was specified."

        if parsed.path not in {"", "/"}:
            return False, "The provided URL cannot contain a subpath."

        return True, f"{parsed.scheme}://{parsed.netloc}"

    async def menu(self, type: typing.Callable, **kwargs) -> str | None:
        return await type(self.ui, **kwargs).run()

    async def run(self) -> None:
        while True:
            response = await self.menu(SelectMenu, options = ["iipython.dev", "(custom)"], **self.prompt(
                "Please select an address to connect to:",
                "If you would like to connect to a custom server, please select \033[32m(custom)\033[0m."
            ))
            if response == "(custom)":
                while True:
                    url = await self.menu(InputMenu, **self.prompt(
                        "Type the address you wish to connect to:",
                        "URL protocol is \033[34moptional\033[0m, if left out it will default to \033[32mhttps://\033[0m."
                    ))
                    if url is None:
                        break

                    success, response = self.normalize(url)
                    if not success:
                        await self.menu(EnterMenu, text = "There was an \033[31missue\033[0m while processing your \033[35mURL\033[0m:\n" +\
                                f"  \033[31m> {response}\033[0m\n\n" +\
                                f"The \033[35mURL\033[0m you provided: \033[90m{url}\033[0m.")

                        continue

                    break

                if url is None:
                    continue

            await self.menu(EnterMenu, text = response)
