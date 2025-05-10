# Copyright (c) 2025 iiPython

# Modules
from pnv3.client import __version__
from pnv3.client.interface import UI, State

async def connect(ui: UI) -> None:
    await ui.set_content("Sure, I'll connect. If you insist ig.")

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
                "func": connect
            }
        }
    ))
    await ui.render()
