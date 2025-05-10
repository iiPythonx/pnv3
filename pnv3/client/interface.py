# Copyright (c) 2025 iiPython

# Modules
import os
import sys
import typing
import asyncio
import textwrap

# Typing
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

        self.lines = []
        for manual_line in self.content.splitlines():
            self.lines += textwrap.wrap(manual_line, width = x - 6) if manual_line.strip() else [manual_line]

        self.length, self._should_wrap = len(self.lines), False

def pad(line: str, width: int) -> str:
    return f"{line}{' ' * (width - len(line))}"

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

        sys.stdout.write(f"├{horizontal_line}┤\n")
        sys.stdout.write(f"│ {pad(' | '.join(action['name'] for action in self.state.actions.values()), cols - 11)} E[x]it │\n")
        sys.stdout.write(f"╰{horizontal_line}╯")
        sys.stdout.flush()

    # State adjustments
    async def propagate(self, key: str) -> None:
        if self.state is None:
            return

        match key.upper():
            case "DN" if self.scroll <= self.state.length - self.terminal_size[1] + 3:
                self.scroll += 1

            case "UP" if self.scroll:
                self.scroll -= 1

            case "X":
                raise KeyboardInterrupt

            case _ as k if k in self.state.actions:
                await self.state.actions[k]["func"](self)

        await self.render()

    def set_state(self, state: State) -> None:
        self.state, self.scroll = state, 0

    async def set_content(self, content: str) -> None:
        if self.state is None:
            raise RuntimeError("Cannot update the content of an empty state!")

        self.state.content = content
        self.state.set_wrap()

        # Re-render new content
        self.scroll = 0
        await self.render()
