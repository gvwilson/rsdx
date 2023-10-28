"""Represent 2D grid."""

from abc import ABC, abstractmethod
import random


class GridGeneric(ABC):
    """Represent a generic grid."""

    @abstractmethod
    def __getitem__(self, key):
        """Get value at location."""

    @abstractmethod
    def __setitem__(self, key, value):
        """Set value at location."""

    def __init__(self, width, height, depth):
        """Record shared state."""
        self._width = width
        self._height = height
        self._depth = depth

    def width(self):
        """Get width of grid."""
        return self._width

    def height(self):
        """Get height of grid."""
        return self._height

    def depth(self):
        """Get depth of grid."""
        return self._depth

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
        return x, y

    def choose_cell(self):
        """Choose the next cell to fill."""
        least, candidates = None, None
        for x in range(self.width()):
            for y in range(self.height()):
                if self[x, y] == 0:
                    continue
                if not self.adjacent(x, y):
                    continue
                if (least is None) or (self[x, y] < least):
                    least = self[x, y]
                    candidates = [(x, y)]
                elif self[x, y] == least:
                    candidates.append((x, y))
        candidates.sort()
        return random.choice(candidates)
