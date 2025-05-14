# Copyright (c) 2025 iiPython

# Modules
from pnv3 import __version__
from pnv3.client.interface import UI, State

from .welcome import WelcomeFlow
from .connection import ConnectionFlow

# Constants
WELCOME_PAGE = f"""\
            <green> _____ _____ _____ ___  
            <green>|  _  |   | |  |  |_  | 
            <green>|   __| | | |  |  |_  | 
            <green>|__|  |_|___|\\___/|___|
                       
                      PNV3
  A continuation of the original PyNet v3 project.

          You are running client <magenta>v{__version__}</>.
       Press <blue>[C]</> to connect, <blue>[C+X]</> to exit.
"""

# Initialization
async def connect(ui: UI) -> None:
    await ConnectionFlow(ui, await WelcomeFlow(ui).run()).run()

async def flow(ui: UI) -> None:
    await ui.set_state(State(
        WELCOME_PAGE,
        {
            "C": {
                "name": "[C]onnect",
                "func": connect(ui)
            }
        }
    ))
