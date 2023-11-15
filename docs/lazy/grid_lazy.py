"""Lazy-filling grid."""

import random

from grid_list import GridList


class GridLazy(GridList):
    """Only look at cells that might actually be filled next time."""

    def __init__(self, width, height, depth):
        """Construct and fill."""
        super().__init__(width, height, depth)
        self._candidates = {}

    def fill_first_cell(self):
        """Fill the initial cell."""
        x, y = super().fill_first_cell()
        self.add_candidates(x, y)

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
        if (x < 0) or (x >= self.width()) or (y < 0) or (y >= self.height()):
            return
        if self[x, y] == 0:
            return

        value = self[x, y]
        if value not in self._candidates:
            self._candidates[value] = set()
        self._candidates[value].add((x, y))
