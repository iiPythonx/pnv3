# Copyright (c) 2025 iiPython

# Modules
import os
import sys
import typing
import asyncio

from pnv3.client import xlen
from pnv3.client.lib.xtract import escape, wrap

# Initialization
class State:
    def __init__(self, content: str, actions: dict[str, dict]) -> None:
        self.content, self.actions = content, actions
        self.rendered = False

        self.lines:     list[str]
        self.length:    int

        # Handle wrapping status
        self._should_wrap: bool
        self.set_wrap()

    def set_wrap(self) -> None:
        self._should_wrap = True

    def wrap(self, x: int) -> None:
        if not self._should_wrap:
            return

        self.lines = escape(wrap(self.content, x - 6))
        self.length, self._should_wrap = len(self.lines), False

def pad(line: str, width: int) -> str:
    return f"{line}{' ' * (width - xlen(line))}"

# Main class
class UI:
    def __init__(self) -> None:
        self.state: typing.Optional[State] = None
        self.scroll: int = 0

        self._propagate_handlers: list[typing.Callable] = []

        self.terminal_size: tuple[int, int] = (0, 0)
        self._last_terminal_size: typing.Optional[tuple[int, int]] = None

    async def _get_terminal_size(self, force: bool = False) -> None:
        size = os.get_terminal_size()
        if self._last_terminal_size and (size != self._last_terminal_size):
            self.terminal_size = size
            await self.render(force = True)

        self._last_terminal_size = size
        if force:
            self.terminal_size = size

    async def watch_terminal(self) -> None:
        while True:
            await self._get_terminal_size()
            await asyncio.sleep(.5)

    async def render(self, force: bool = False) -> None:
        if self.state is None:
            raise RuntimeError("Cannot render an empty state!")

        if self.terminal_size == (0, 0):
            await self._get_terminal_size(force = True)

        cols, rows = self.terminal_size
        self.state.wrap(cols - 2)

        # Handle drawing content
        def draw_content() -> None:
            visible_lines = self.state.lines[self.scroll:self.scroll + rows - 4]  # type: ignore
            line_count = len(visible_lines)

            width = cols - 9  # TODO: make a customizable sidebar system that autocalculates this
            for i in range(rows - 4):
                line = visible_lines[i] if i < line_count else ""
                sys.stdout.write(f"│ {str(self.scroll + i + 1).zfill(2)} │ {pad(line, width)} │\n")  # type: ignore

        if self.state.rendered and not force:

            # We've already been rendered once before, therefore we only
            # need to rerender the content and not the entire screen.
            sys.stdout.write("\033[2;1H")
            draw_content()
            return sys.stdout.flush()

        horizontal_line = "─" * (cols - 2)

        sys.stdout.write(f"\033[H\033[2J╭{horizontal_line}╮\n")

        draw_content()
        self.state.rendered = True

        action_layout = " | ".join(f"\033[35m{action['name']}\033[0m" for action in self.state.actions.values())

        sys.stdout.write(f"├{horizontal_line}┤\n")
        sys.stdout.write(f"│ {pad(action_layout, cols - 15)} \033[31m[C+X] Exit\033[0m │\n")
        sys.stdout.write(f"╰{horizontal_line}╯")
        sys.stdout.flush()

    # Propagation handlers
    def on_propagate(self, function: typing.Callable) -> None:
        self._propagate_handlers.append(function)

    def remove_propagate(self, function: typing.Callable) -> None:
        self._propagate_handlers.remove(function)

    async def propagate(self, key: str) -> None:
        if self.state is None:
            return

        match key:
            case "DN" if self.scroll <= self.state.length - self.terminal_size[1] + 3:
                self.scroll += 1

            case "UP" if self.scroll:
                self.scroll -= 1

            case "\x18":
                raise KeyboardInterrupt  # CTRL+X

            case _:
                upper = key.upper()
                if upper in self.state.actions:
                    asyncio.create_task(self.state.actions[upper]["func"])

                else:
                    for handler in self._propagate_handlers:
                        await handler(key)

        await self.render()

    # State adjustments
    async def set_state(self, state: State) -> None:
        self.state, self.scroll = state, 0
        await self.render()

    async def set_content(self, content: str) -> None:
        if self.state is None:
            raise RuntimeError("Cannot update the content of an empty state!")

        self.state.content = content
        self.state.set_wrap()

        # Re-render new content
        self.scroll = 0
        await self.render()

    # Handle actions
    def get_actions(self) -> dict[str, dict]:
        if self.state is None:
            raise RuntimeError("Cannot fetch the actions of an empty state!")

        return self.state.actions

    async def set_actions(self, actions: dict[str, dict]) -> None:
        if self.state is None:
            raise RuntimeError("Cannot set the actions of an empty state!")

        self.state.actions = actions
        await self.render(force = True)
