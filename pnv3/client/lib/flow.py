# Copyright (c) 2025 iiPython

# Modules
from pnv3.client import __version__
from pnv3.client.interface import UI, State

from pnv3.client.flows import ConnectionFlow

# Constants
WELCOME_PAGE = f"""\
            \033[32m _____ _____ _____ ___  \033[0m
            \033[32m|  _  |   | |  |  |_  | \033[0m
            \033[32m|   __| | | |  |  |_  | \033[0m
            \033[32m|__|  |_|___|\\___/|___|\033[0m
                       
                      PNV3
  A continuation of the original PyNet v3 project.

          You are running client \033[35mv{__version__}\033[0m.
       Press \033[34m[C]\033[0m to connect, \033[34m[C+X]\033[0m to exit.
"""

# Initialization
async def flow(ui: UI) -> None:
    await ui.set_state(State(
        WELCOME_PAGE,
        {
            "C": {
                "name": "[C]onnect",
                "func": ConnectionFlow(ui).run
            }
        }
    ))
