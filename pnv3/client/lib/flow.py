# Copyright (c) 2025 iiPython

# Modules
from pnv3.client import __version__, xlen
from pnv3.client.interface import UI, State

from pnv3.client.objects import InputMenu, SelectMenu

# Initialization
SELECT_BOTTOM = "If you would like to connect to a custom server, please select \033[32m(custom)\033[0m."
SELECT_ARGS = [
    "Please select an address to connect to:",
    ["iipython.dev", "(custom)"],
    f"{'─' * xlen(SELECT_BOTTOM)}\n{SELECT_BOTTOM}"
]

INPUT_BOTTOM = "URL protocol is \033[34moptional\033[0m, if left out it will default to \033[32mhttps://\033[0m."
INPUT_ARGS = [
    "Type the address you wish to connect to:",
    f"{'─' * xlen(INPUT_BOTTOM)}\n{INPUT_BOTTOM}"    
]

async def connect_state(ui: UI) -> None:
    while True:
        response = await SelectMenu(ui, *SELECT_ARGS).run()
        if response == "(custom)":
            response = await InputMenu(ui, *INPUT_ARGS).run()

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
