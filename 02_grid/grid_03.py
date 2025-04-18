import csv
import io
import random
import sys


class Grid:
    """Store a grid of numbers."""

    def __init__(self, size):
        """Construct empty grid."""
        assert size > 0, f"Grid size must be positive not {size}"
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]

    def __getitem__(self, key):
        """Get grid element."""
        x, y = key
        return self.grid[x][y]

    def __setitem__(self, key, value):
        """Set grid element."""
        x, y = key
        self.grid[x][y] = value

    def __str__(self):
        """Convert to string."""
        output = io.StringIO()
        csv.writer(output).writerows(self.grid)
        return output.getvalue()


def fill_grid(grid):
    """Fill in a grid."""

    moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    center = grid.size // 2
    size_1 = grid.size - 1
    x, y = center, center
    while (x != 0) and (y != 0) and (x != size_1) and (y != size_1):
        grid[x, y] += 1
        m = random.choice(moves)
        x += m[0]
        y += m[1]


if __name__ == "__main__":
    size = int(sys.argv[1])
    seed = int(sys.argv[2])
    random.seed(seed)
    grid = Grid(size)
    fill_grid(grid)
    print(grid)
