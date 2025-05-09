# Copyright (c) 2025 iiPython

# Modules
import os
import signal
import asyncio

from pnv3.client import interface
from pnv3.client.lib import keypress

# Initialization
ui, stop = interface.UI(), asyncio.Event()

def handle_sigint() -> None:
    stop.set()

def exit_interface() -> None:
    print("Bai bai!\033[?1049l\033[?25h")
    os._exit(0)

async def keypress_loop(ui: interface.UI) -> None:
    try:
        while True:
            await ui.propagate(await keypress.read())

    except asyncio.CancelledError:
        return

async def main() -> None:
    tasks = [
        asyncio.create_task(ui.watch_terminal()),
        asyncio.create_task(keypress_loop(ui))
    ]
    if os.name != "nt":
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, handle_sigint)  # Ctrl+C

    print("\033[?1049h\033[?25l")

    ui.set_state(interface.State("hello\nworld\nthis\nis\na\ntest\npage\ndesigned\nto\ntest\nmy\nscrolling\nsetup\nhopefully\nit\nworks\nwithout\nissues"))
    await ui.render()

    await stop.wait()
    [task.cancel() for task in tasks]

    for task in tasks:
        try:
            await task

        except asyncio.CancelledError:
            pass  # This is fine.

    exit_interface()

try:
    asyncio.run(main())

except KeyboardInterrupt:
    exit_interface()
