import argparse
import csv
import io
import random


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


def cmdline_args():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, required=True, help="RNG seed")
    parser.add_argument("--size", type=int, required=True, help="grid size")
    return parser.parse_args()


def fill_grid(grid):
    """Fill in a grid."""

    moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    center = grid.size // 2
    size_1 = grid.size - 1
    x, y = center, center
    num = 0

    while (x != 0) and (y != 0) and (x != size_1) and (y != size_1):
        grid[x, y] += 1
        num += 1
        m = random.choice(moves)
        x += m[0]
        y += m[1]

    return num


if __name__ == "__main__":
    args = cmdline_args()
    random.seed(args.seed)
    grid = Grid(args.size)
    fill_grid(grid)
    print(grid)
