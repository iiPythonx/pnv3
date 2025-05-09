# Copyright (c) 2025 iiPython

# Modules
import os
import sys
import typing
import asyncio
import textwrap

# Typing
class State:
    def __init__(self, content: str) -> None:
        self.content = content

        self.lines:     list[str]
        self.length:    int
        self.max_zfill: int

    def wrap(self, x: int) -> None:
        self.lines = []
        for manual_line in self.content.splitlines():
            self.lines += textwrap.wrap(manual_line, width = x)

        self.length = len(self.lines)
        self.max_zfill = len(str(self.length))

# Main class
class UI:
    def __init__(self) -> None:
        self.state: typing.Optional[State] = None
        self.scroll: int = 0

        self.terminal_size: tuple[int, int] = (0, 0)
        self._last_terminal_size: typing.Optional[tuple[int, int]] = None

    async def _get_terminal_size(self, force: bool = False) -> None:
        size = os.get_terminal_size()
        if self._last_terminal_size and (size != self._last_terminal_size):
            self.terminal_size = size
            print(f"[TERMSIZE] Updated to {size}")
            await self.render()

        self._last_terminal_size = size
        if force:
            self.terminal_size = size

    async def watch_terminal(self) -> None:
        while True:
            await self._get_terminal_size()
            await asyncio.sleep(.5)

    async def render(self) -> None:
        if self.state is None:
            raise RuntimeError("Cannot render an empty state!")

        if self.terminal_size == (0, 0):
            await self._get_terminal_size(force = True)

        cols, rows = self.terminal_size
        horizontal_line = "─" * (cols - 2)

        sys.stdout.write("\033[H\033[2J")
        sys.stdout.write(f"╭{horizontal_line}╮\n")

        self.state.wrap(cols - 2)

        visible_lines = self.state.lines[self.scroll:self.scroll + rows - 4]
        line_count = len(visible_lines)

        for i in range(rows - 4):
            actual_index = self.scroll + i
            line = visible_lines[i] if i < line_count else ""
            sys.stdout.write(f"│ {str(actual_index + 1).zfill(self.state.max_zfill)} │ {line}\n")

        sys.stdout.write(f"├{horizontal_line}┤\n")
        sys.stdout.write("│ [E]xit │\n")
        sys.stdout.write(f"╰{horizontal_line}╯")
        sys.stdout.flush()

    # State adjustments
    async def propagate(self, key: str) -> None:
        match key:
            case "DN" if (self.state is not None) and (self.scroll <= self.state.length - self.terminal_size[1] + 3):
                self.scroll += 1

            case "UP" if self.scroll:
                self.scroll -= 1

        await self.render()

    def set_state(self, state: State) -> None:
        self.state = state
