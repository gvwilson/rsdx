"""Represent 2D grid."""

import sys


class Grid:
    """Represent a grid."""

    UNINIT = -1
    FILLED = 0

    def __init__(self, width, height, depth, values=None):
        """Construct and fill."""
        self._width = width
        self._height = height
        self._depth = depth
        self._grid = [[self.UNINIT] * self._height for _ in range(self._width)]
        if values is not None:
            self.overwrite(values)

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
        assert (value == Grid.FILLED) or (1 <= value <= self._depth)
        self._grid[x][y] = value

    def __eq__(self, other):
        """Compare to another grid."""
        if self._width != other.width():
            return False
        if self._height != other.height():
            return False
        for x, y, val in self.sweep():
            if val != other[x, y]:
                return False
        return True

    def sweep(self):
        """Return indices and values in order."""
        for x in range(self._width):
            for y in range(self._height):
                yield (x, y, self._grid[x][y])

    def on_border(self, x, y):
        """Is this cell on the border of the grid?"""
        if (x == 0) or (x == self._width - 1):
            return True
        if (y == 0) or (y == self._height - 1):
            return True
        return False

    def print(self, stream=sys.stdout, details="full"):
        """Show the result."""
        print(self._width, self._height, self._depth, file=stream)
        if details == "brief":
            return
        for y in range(self._height - 1, -1, -1):
            for x in range(self._width):
                if details == "numbers":
                    stream.write(f"{self[x, y]:02d} ")
                else:
                    stream.write("X" if self[x, y] == self.FILLED else ".")
            stream.write("\n")

    def overwrite(self, values):
        """Overwrite with values."""
        assert len(values) == self._width
        assert all(len(v) == self._height for v in values)
        self._grid = [v[:] for v in values]
