# Copyright (c) 2025 iiPython
# Pure async keypress solution

# Modules
import os
import asyncio
from typing import Callable

# Handle platform specifics
MAPPING = {
    "\x1b]A": "UP",
    "\x1b]B": "DN",
    "\x1b]C": "RI",
    "\x1b]D": "LE",
}

def setup_linux() -> Callable:
    import tty
    import sys
    import termios

    async def read() -> str:
        loop = asyncio.get_event_loop()

        fd = sys.stdin.fileno()
        settings = termios.tcgetattr(fd)
        
        buffer = []
        try:
            tty.setcbreak(fd)
            while True:
                char = await loop.run_in_executor(None, sys.stdin.read, 1)
                if char == "\x1b":
                    buffer.append(char)
                    continue

                elif buffer:
                    if char == "[":
                        continue

                    char = f"\x1b]{char}"
                    return MAPPING.get(char, char)

                elif char:
                    return char

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, settings)

    return read

def setup_windows():
    import msvcrt

    async def read() -> str:
        loop = asyncio.get_event_loop()
        def get_char():
            return msvcrt.getwch() if msvcrt.kbhit() else None

        while True:
            char = await loop.run_in_executor(None, get_char)
            if char:
                return char

            await asyncio.sleep(0.01)

    return read

read = (setup_linux if os.name == "posix" else setup_windows)()
