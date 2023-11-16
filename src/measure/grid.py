"""Represent 2D grid."""

import random
import sys


class Grid:
    """Represent a grid."""

    def __init__(self, width, height, depth):
        """Construct and fill."""
        self._width = width
        self._height = height
        self._depth = depth
        self._grid = self._init_grid()
        self._candidates = {}

    def width(self):
        """Get width of grid."""
        return self._width

    def height(self):
        """Get height of grid."""
        return self._height

    def depth(self):
        """Get depth of grid."""
        return self._depth

    def contents(self):
        """Get grid content."""
        return self._grid

    def __getitem__(self, key):
        """Get value at location."""
        x, y = key
        return self._grid[x][y]

    def __setitem__(self, key, value):
        """Set value at location."""
        x, y = key
        self._grid[x][y] = value

    def __eq__(self, other):
        """Compare to another grid."""
        if self.width() != other.width():
            return False
        if self.height() != other.height():
            return False
        for x in range(self.width()):
            for y in range(self.height()):
                if self[x, y] != other[x, y]:
                    return False
        return True

    def fill(self):
        """Fill grid one cell at a time."""
        self.fill_first_cell()
        while True:
            x, y = self.choose_cell()
            self[x, y] = 0
            if self.on_border(x, y):
                break

    def adjacent(self, x, y):
        """Is (x, y) adjacent to a filled cell?"""
        x_1, y_1 = x + 1, y + 1
        if (x > 0) and (self[x - 1, y] == 0):
            return True
        if (x_1 < self.width()) and (self[x_1, y] == 0):
            return True
        if (y > 0) and (self[x, y - 1] == 0):
            return True
        if (y_1 < self.height()) and (self[x, y_1] == 0):
            return True
        return False

    def on_border(self, x, y):
        """Is this cell on the border of the grid?"""
        if (x == 0) or (x == self.width() - 1):
            return True
        if (y == 0) or (y == self.height() - 1):
            return True
        return False

    def fill_first_cell(self):
        """Fill the initial cell."""
        x = self.width() // 2
        y = self.height() // 2
        self[x, y] = 0
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

    def print(self, stream=sys.stdout, details="full"):
        """Show the result."""
        print(self.width(), self.height(), self.depth(), file=stream)
        if details == "brief":
            return
        for y in range(self.height() - 1, -1, -1):
            for x in range(self.width()):
                if details == "numbers":
                    stream.write(f"{self[x, y]:02d} ")
                else:
                    stream.write("X" if self[x, y] == 0 else ".")
            stream.write("\n")

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

    def _init_grid(self):
        """Initialize grid contents."""
        temp = []
        for x in range(self._width):
            row = []
            for y in range(self._height):
                row.append(random.randint(1, self._depth))
            temp.append(row)
        return temp
