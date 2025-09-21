from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Set, Tuple
import random

Coord = Tuple[int, int]


offsets: Tuple[Coord, ...] = (
    (-1, -1), (0, -1), (1, -1),
    (-1,  0),          (1,  0),
    (-1,  1), (0,  1), (1,  1),
)


@dataclass
class Life:
    width: int
    height: int

    def __post_init__(self) -> None:
        # Grid stored as a set of live cell coordinates (x, y)
        self.live: Set[Coord] = set()

    # --- Utilities ---
    def _wrap(self, x: int, y: int) -> Coord:
        return (x % self.width, y % self.height)

    def set_live(self, cells: Iterable[Coord]) -> None:
        for (x, y) in cells:
            self.live.add(self._wrap(x, y))

    def clear(self) -> None:
        self.live.clear()

    # --- Initialization helpers ---
    def randomize(self, density: float = 0.2, rng: random.Random | None = None) -> None:
        """Fill the grid with random live cells with given density (0.0 - 1.0)."""
        assert 0.0 <= density <= 1.0
        rng = rng or random
        self.live = {
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if rng.random() < density
        }

    def set_pattern(self, name: str, x_offset: int | None = None, y_offset: int | None = None) -> None:
        name = name.lower()
        if x_offset is None:
            x_offset = self.width // 2
        if y_offset is None:
            y_offset = self.height // 2

        if name == "glider":
            pattern = {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)}
        elif name == "blinker":
            pattern = {(0, 0), (1, 0), (2, 0)}
        else:
            raise ValueError(f"Unknown pattern: {name}")

        translated = {(x + x_offset, y + y_offset) for (x, y) in pattern}
        self.set_live(translated)

    # --- Simulation step ---
    def step(self) -> None:
        """Advance the world by one generation using Conway's rules (toroidal wrap)."""
        neighbor_counts: dict[Coord, int] = {}

        # Count neighbors only around live cells and their neighbors
        for (x, y) in self.live:
            for dx, dy in offsets:
                n = self._wrap(x + dx, y + dy)
                neighbor_counts[n] = neighbor_counts.get(n, 0) + 1

        new_live: Set[Coord] = set()

        # Cells that have neighbor counts: candidates for life
        for cell, count in neighbor_counts.items():
            if count == 3 or (count == 2 and cell in self.live):
                new_live.add(cell)

        # Also check live cells that had zero counted neighbors (rare); they die anyway
        # so we don't need to explicitly add them.
        self.live = new_live

    # --- Rendering ---
    def render(self, live_char: str = "█", dead_char: str = " ") -> str:
        rows: List[str] = []
        for y in range(self.height):
            row = [live_char if (x, y) in self.live else dead_char for x in range(self.width)]
            rows.append("".join(row))
        return "\n".join(rows)
