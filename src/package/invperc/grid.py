"""Two-dimensional grid that can simulate invasion percolation."""

import random


class Grid:
    """Represent a generic grid.

    This class uses a list-of-lists representation of a rectangular
    grid, and keeps track of candidate cells on the border of the
    already-filled region to make filling faster.
    """

    def __init__(self, width, height, depth):
        """Construct grid.

        Args:
            width: X size of grid (positive integer).
            height: Y size of grid (positive integer).
            depth: range of random grid values (positive integer).
        """
        self._width = width
        self._height = height
        self._depth = depth
        self._init_grid()
        self._candidates = {}

    def __getitem__(self, key):
        """Get value at location.

        Args:
            key: 2-tuple of (x, y) coordinates.

        Returns:
            Value at specified location.
        """
        x, y = key
        return self._grid[x][y]

    def __setitem__(self, key, value):
        """Set value at location.

        Args:
            key: 2-tuple of (x, y) coordinates.
            value: new value for that location.
        """
        x, y = key
        self._grid[x][y] = value

    def __eq__(self, other):
        """Check equality of this grid with another.

        Args:
            other: the other grid to check

        Returns:
            `True` if grids are the same size and contain equal
            values, `False` otherwise.
        """
        if self.width != other.width:
            return False
        if self.height != other.height:
            return False
        for x in range(self.width):
            for y in range(self.height):
                if self[x, y] != other[x, y]:
                    return False
        return True

    def __str__(self):
        """Create string representation of grid.

        Returns:
            `str` showing filled cells as 'X' and empty cells as '.'
        """
        rows = []
        for y in range(self.height - 1, -1, -1):
            row = ("X" if self[x, y] == 0 else "." for x in range(self.width))
            rows.append(''.join(row))
        return "\n".join(rows)

    @property
    def width(self):
        """Width of grid."""
        return self._width

    @property
    def height(self):
        """Height of grid."""
        return self._height

    @property
    def depth(self):
        """Depth of grid."""
        return self._depth

    def fill(self):
        """Fill grid one cell at a time from the center."""
        x, y = self.width // 2, self.height // 2
        self[x, y] = 0
        num_filled = 1
        self._add_candidates(x, y)

        while True:
            x, y = self._choose_cell()
            self[x, y] = 0
            num_filled += 1
            if self._on_border(x, y):
                break
        return num_filled

    def _add_candidates(self, x, y):
        """Add candidates around specified coordinate.

        Args:
            x: X-axis coordinate of cell whose neighbors are checked.
            y: Y-axis coordinate of cell whose neighbors are checked.
        """
        for ix in (x - 1, x + 1):
            self._add_one_candidate(ix, y)
        for iy in (y - 1, y + 1):
            self._add_one_candidate(x, iy)

    def _add_one_candidate(self, x, y):
        """Potentially add a single cell to the set of candidates.

        Args:
            x: X-axis coordinate of cell whose neighbors are checked.
            y: Y-axis coordinate of cell whose neighbors are checked.
        """
        if (x < 0) or (x >= self.width) or (y < 0) or (y >= self.height):
            return
        if self[x, y] == 0:
            return
        value = self[x, y]
        if value not in self._candidates:
            self._candidates[value] = set()
        self._candidates[value].add((x, y))

    def _choose_cell(self):
        """Choose the next cell to fill.

        All cells on the boundary of the filled region whose value is
        equal to the lowest value of any cell on the boundary are
        candidates for filling; one of these cells is chosen at
        random.
        """
        min_key = min(self._candidates.keys())
        available = list(sorted(self._candidates[min_key]))
        i = random.randrange(len(available))
        choice = available[i]
        del available[i]
        if not available:
            del self._candidates[min_key]
        else:
            self._candidates[min_key] = set(available)
        self._add_candidates(*choice)
        return choice

    def _init_grid(self):
        """Create and fill list-of-lists grid."""
        self._grid = []
        for x in range(self.width):
            row = []
            for y in range(self.height):
                row.append(random.randint(1, self.depth))
            self._grid.append(row)

    def _on_border(self, x, y):
        """Check whether a cell is on the border of the grid.

        Args:
            x: X-axis coordinate of cell to check.
            y: Y-axis coordinate of cell to check.
        """
        if (x == 0) or (x == self.width - 1):
            return True
        if (y == 0) or (y == self.height - 1):
            return True
        return False
