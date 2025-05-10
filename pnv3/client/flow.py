# Copyright (c) 2025 iiPython

# Modules
import logging

from pnv3.client import __version__, xlen
from pnv3.client.interface import UI, State

from pnv3.client.lib.input import InputMenu
from pnv3.client.lib.select import SelectMenu

async def connect_state(ui: UI) -> None:
    bottom = "If you would like to connect to a custom server, please select \033[32m(custom)\033[0m."
    while True:
        response = await SelectMenu(ui, "Please select an address to connect to:", ["iipython.dev", "(custom)"], f"{'─' * xlen(bottom)}\n{bottom}").run()
        if response == "(custom)":
            response = await InputMenu(ui, "Type the address you wish to connect to:").run()

async def flow(ui: UI) -> None:
    ui.set_state(State(
        f"""
    ░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓████████▓▒░▒▓████████▓▒░
    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░         ░▒▓█▓▒░
    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░         ░▒▓█▓▒░
    ░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░    ░▒▓█▓▒░
    ░▒▓█▓▒░         ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░         ░▒▓█▓▒░
    ░▒▓█▓▒░         ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░         ░▒▓█▓▒░
    ░▒▓█▓▒░         ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░  ░▒▓█▓▒░

                WELCOME TO PYNET, CLIENT VERSION {__version__}
                  PRESS [C] TO CONNECT, [X] TO EXIT.
        """,
        {
            "C": {
                "name": "[C]onnect",
                "func": connect_state
            }
        }
    ))
    await ui.render()
