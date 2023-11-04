"""Represent 2D grid."""

import random
import sys


class Grid:
    """Represent a grid."""

    UNINIT = -1
    FILLED = 0

    def __init__(self, width, height, depth):
        """Construct and fill."""
        self._width = width
        self._height = height
        self._depth = depth
        self._grid = [
            [self.UNINIT] * self._height
            for _ in range(self._width)
        ]

    def width(self):
        """Get width of grid."""
        return self._width

    def height(self):
        """Get height of grid."""
        return self._height

    def depth(self):
        """Get depth of grid."""
        return self._depth

    def __getitem__(self, key):
        """Get value at location."""
        x, y = key
        assert 0 <= x < self._width
        assert 0 <= y < self._height
        assert self._grid[x][y] != self.UNINIT
        return self._grid[x][y]

    def __setitem__(self, key, value):
        """Set value at location."""
        x, y = key
        assert 0 <= x < self._width
        assert 0 <= y < self._height
        assert 0 <= value <= self._depth
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

    def adjacent(self, x, y):
        """Is (x, y) adjacent to a filled cell?"""
        x_1, y_1 = x + 1, y + 1
        if (x > 0) and (self[x - 1, y] == FILLED):
            return True
        if (x_1 < self.width()) and (self[x_1, y] == FILLED):
            return True
        if (y > 0) and (self[x, y - 1] == FILLED):
            return True
        if (y_1 < self.height()) and (self[x, y_1] == FILLED):
            return True
        return False

    def on_border(self, x, y):
        """Is this cell on the border of the grid?"""
        if (x == 0) or (x == self.width() - 1):
            return True
        if (y == 0) or (y == self.height() - 1):
            return True
        return False

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
                    stream.write("X" if self[x, y] == FILLED else ".")
            stream.write("\n")
