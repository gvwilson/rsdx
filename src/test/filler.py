"""Manage filling."""

import random


class Filler:
    """Manage grid filling."""

    def __init__(self, grid):
        """Construct."""
        self._grid = grid
        self._candidates = {}

    def grid(self):
        """Get the grid object."""
        return self._grid

    def fill(self, randomize=True):
        """Fill grid one cell at a time."""
        if randomize:
            self._randomize()
        self.fill_first_cell()
        while True:
            x, y = self.choose_cell()
            self._grid[x, y] = self._grid.FILLED
            if self._grid.on_border(x, y):
                break

    def fill_first_cell(self):
        """Fill the initial cell."""
        x = self._grid.width() // 2
        y = self._grid.height() // 2
        self._grid[x, y] = self._grid.FILLED
        self.add_candidates(x, y)
        return x, y

    def choose_cell(self):
        """Choose the next cell to fill."""
        min_key = min(self._candidates.keys())
        available = list(self._candidates[min_key])
        available.sort()
        choice = random.choice(available)
        available = set(available)
        available.remove(choice)
        if not available:
            del self._candidates[min_key]
        else:
            self._candidates[min_key] = available
        self.add_candidates(*choice)
        return choice

    def add_candidates(self, x, y):
        """Add candidates around (x, y)."""
        for ix in (x - 1, x + 1):
            self._add_candidate(ix, y)
        for iy in (y - 1, y + 1):
            self._add_candidate(x, iy)

    def _add_candidate(self, x, y):
        """Add (x, y) if suitable."""
        if (
            (x < 0)
            or (x >= self._grid.width())
            or (y < 0)
            or (y >= self._grid.height())
        ):
            return

        if self._grid[x, y] == self._grid.FILLED:
            return

        value = self._grid[x, y]
        if value not in self._candidates:
            self._candidates[value] = set()
        self._candidates[value].add((x, y))

    def _randomize(self):
        """Randomize grid contents."""
        for x, y, _ in self._grid.sweep():
            self._grid[x, y] = random.randint(1, self._grid.depth())
