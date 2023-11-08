"""Invasion percolation in Python."""

import random
import sys

from grid_list import GridList
from grid_array import GridArray


def main():
    """Main driver."""
    kind, width, height, depth, seed = setup()
    grid = initialize_grid(kind, width, height, depth)
    fill_grid(grid)
    print_grid(kind, grid, seed)


def setup():
    """Get parameters."""
    kind = sys.argv[1]
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    depth = int(sys.argv[4])

    if len(sys.argv) > 5:
        seed = int(sys.argv[5])
    else:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)

    return kind, width, height, depth, seed


def initialize_grid(kind, width, height, depth):
    """Prepare grid for simulation."""
    lookup = {
        "list": GridList,
        "array": GridArray,
    }
    return lookup[kind](width, height, depth)


def fill_grid(grid):
    """Fill grid one cell at a time."""
    grid[grid.width() // 2, grid.height() // 2] = 0
    while True:
        x, y = choose_cell(grid)
        grid[x, y] = 0
        if grid.on_border(x, y):
            break


def choose_cell(grid):
    """Choose the next cell to fill."""
    least, cx, cy = None, None, None
    for x in range(grid.width()):
        for y in range(grid.height()):
            temp = grid[x, y]
            if not grid.adjacent(x, y):
                continue
            if (least is None) or ((temp != 0) and (temp < least)):
                least, cx, cy = temp, x, y
    return cx, cy


def print_grid(kind, grid, seed, details="full"):
    """Show the result."""
    print(kind, grid.width(), grid.height(), grid.depth(), seed)
    if details == "brief":
        return
    for y in range(grid.height() - 1, -1, -1):
        for x in range(grid.width()):
            if details == "numbers":
                sys.stdout.write(f"{grid[x, y]:02d} ")
            else:
                sys.stdout.write("X" if grid[x, y] == 0 else ".")
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
