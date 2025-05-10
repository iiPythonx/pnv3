# Copyright (c) 2025 iiPython

# Modules
import os
import signal
import typing
import asyncio
import traceback

from pnv3.client import interface
from pnv3.client.flow import flow
from pnv3.client.lib import keypress

# Initialization
ui, stop = interface.UI(), asyncio.Event()

def handle_sigint() -> None:
    stop.set()

def exit_interface(exception: typing.Optional[Exception] = None) -> None:
    print("\033[?1049l\033[?25h", end = "")
    if exception is not None:
        print(traceback.format_exc())
        print("Report this at https://github.com/iiPythonx/pnv3.")

    else:
        print("Bai bai!")

    os._exit(0)

async def keypress_loop(ui: interface.UI) -> None:
    try:
        while True:
            await ui.propagate(await keypress.read())

    except asyncio.CancelledError:
        return

async def main() -> None:
    if os.name != "nt":
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, handle_sigint)  # Ctrl+C

    print("\033[?1049h\033[?25l")
    try:
        tasks = [
            asyncio.create_task(ui.watch_terminal()),
            asyncio.create_task(keypress_loop(ui)),
            asyncio.create_task(flow(ui))
        ]
        await stop.wait()

        for task in tasks:
            try:
                task.cancel()
                await task

            except asyncio.CancelledError:
                pass  # This is fine.

    except Exception as e:
        return exit_interface(e)

    exit_interface()

try:
    asyncio.run(main())

except KeyboardInterrupt:
    exit_interface()
