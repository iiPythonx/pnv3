# Copyright (c) 2025 iiPython

# Modules
from urllib.parse import urlparse

from pnv3.client import __version__, xlen
from pnv3.client.interface import UI, State
from pnv3.client.objects import InputMenu, SelectMenu, EnterMenu

# Initialization
def generic_prompt(text: str, footer: str) -> dict[str, str]:
    return {
        "prompt": text,
        "footer": f"{'─' * xlen(footer)}\n{footer}"
    }

def normalize_url(url: str) -> tuple[bool, str]:
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

async def connect_state(ui: UI) -> None:
    while True:
        response = await SelectMenu(ui, options = ["iipython.dev", "(custom)"], **generic_prompt(
            "Please select an address to connect to:",
            "If you would like to connect to a custom server, please select \033[32m(custom)\033[0m."
        )).run()
        if response == "(custom)":
            while True:
                url = await InputMenu(ui, **generic_prompt(
                    "Type the address you wish to connect to:",
                    "URL protocol is \033[34moptional\033[0m, if left out it will default to \033[32mhttps://\033[0m."
                )).run()
                if url is None:
                    break

                success, response = normalize_url(url)
                if not success:
                    await EnterMenu(ui, "There was an \033[31missue\033[0m while processing your \033[35mURL\033[0m:\n" +\
                            f"  \033[31m> {response}\033[0m\n\n" +\
                            f"The \033[35mURL\033[0m you provided: \033[90m{url}\033[0m.").run()

                    continue

                break

            if url is None:
                continue

        await EnterMenu(ui, response).run()

async def flow(ui: UI) -> None:
    ui.set_state(State(
        f"""             \033[32m_____ _____ _____ ___ \033[0m
            \033[32m|  _  |   | |  |  |_  |\033[0m
            \033[32m|   __| | | |  |  |_  |\033[0m
            \033[32m|__|  |_|___|\\___/|___|\033[0m
                       
                      PNV3
  A continuation of the original PyNet v3 project.

          You are running client \033[35mv{__version__}\033[0m.
       Press \033[34m[C]\033[0m to connect, \033[34m[C+X]\033[0m to exit.
        """,
        {
            "C": {
                "name": "[C]onnect",
                "func": connect_state
            }
        }
    ))
    await ui.render()
