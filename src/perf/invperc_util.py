"""Invasion percolation implementation utilities."""

import json
from pathlib import Path
import random
import sys

from grid_list import GridList
from grid_array import GridArray


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


def fill_grid(grid):
    """Fill grid one cell at a time."""
    grid[grid.width() // 2, grid.height() // 2] = 0
    num_filled = 1
    while True:
        x, y = choose_cell(grid)
        grid[x, y] = 0
        num_filled += 1
        if grid.on_border(x, y):
            break
    return num_filled


def initialize_grid(params):
    """Prepare grid for simulation."""
    lookup = {
        "list": GridList,
        "array": GridArray,
    }
    assert params.kind in lookup, f"Unknown grid type {kind}"
    cls = lookup[params.kind]
    return cls(params.width, params.height, params.depth)


def initialize_random(params):
    """Initialize random number generation."""
    if params.seed is None:
        params.random.randrange(sys.maxsize)
    random.seed(params.seed)


def print_grid(params, grid, num_filled, details="brief"):
    """Show the result."""
    print(params.kind, params.width, params.depth, params.seed, num_filled)
    if details == "brief":
        return
    for y in range(grid.height() - 1, -1, -1):
        for x in range(grid.width()):
            if details == "numbers":
                sys.stdout.write(f"{grid[x, y]:02d} ")
            else:
                sys.stdout.write("X" if grid[x, y] == 0 else ".")
        sys.stdout.write("\n")


def setup(cls):
    """Get parameters."""
    assert len(sys.argv) == 2, "Usage: invperc.py params_file.json"
    with open(sys.argv[1], "r") as reader:
        d = json.load(reader)
        return cls(**d)
