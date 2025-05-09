# Copyright (c) 2025 iiPython

# Modules
import asyncio

from pnv3.client import interface
from pnv3.client.lib import keypress

# Initialization
ui = interface.UI()

# Handle event loop
async def daemon() -> None:
    while True:
        print(await keypress.read())

async def main() -> None:
    asyncio.create_task(daemon())
    while True:
        print("hi")
        await asyncio.sleep(1)

asyncio.run(main())
