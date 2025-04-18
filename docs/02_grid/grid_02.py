import csv
import random
import sys


def make_grid(size):
    """Create and fill a square of the specified size."""

    # Make an empty grid
    grid = []
    for i in range(size):
        grid.append([0 for _ in range(size)])

    # Prep
    center = size // 2
    size_1 = size - 1
    moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]

    # Move and fill until we reach the edge
    x, y = center, center
    while (x != 0) and (y != 0) and (x != size_1) and (y != size_1):
        grid[x][y] += 1
        m = random.choice(moves)
        x += m[0]
        y += m[1]

    return grid


if __name__ == "__main__":
    size = int(sys.argv[1])
    seed = int(sys.argv[2])
    random.seed(seed)
    grid = make_grid(size)
    csv.writer(sys.stdout).writerows(grid)
