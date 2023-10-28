"""Invasion percolation in Python."""

import argparse
import random
import numpy as np
import pandas as pd
import sys

from grid_lazy import GridLazy


def main():
    """Main driver."""
    args = setup()
    initialize_random(args.seed)
    results = percolate(args)
    dim = -np.polyfit(np.log(results["ruler"]), np.log(results["count"]), 1)[0]
    print(dim)
    if args.details:
        with open(args.details, "w") as writer:
            print(results.to_csv(index=False), file=writer)


def setup():
    """Get parameters."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", type=int, default=2, help="depth")
    parser.add_argument("--details", type=str, default=None, help="output file")
    parser.add_argument("--size", type=int, default=3, help="size")
    parser.add_argument("--reps", type=int, default=1, help="repetitions")
    parser.add_argument("--seed", type=int, default=None, help="RNG seed")
    args = parser.parse_args()
    args.width = args.height = args.size
    return args


def initialize_random(seed=None):
    if seed is None:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    return seed


def percolate(args):
    result = []
    for _ in range(args.reps):
        seed = initialize_random()
        grid = GridLazy(args.width, args.height, args.depth)
        fill_grid(grid)
        dims = measure_dimension(grid)
        result.extend([(args.size, args.depth, seed, *d) for d in dims])
    return pd.DataFrame(result, columns=("size", "depth", "seed", "ruler", "count"))


def fill_grid(grid):
    """Fill grid one cell at a time."""
    grid.fill_first_cell()
    while True:
        x, y = grid.choose_cell()
        grid[x, y] = 0
        if grid.on_border(x, y):
            break


def measure_dimension(grid):
    """Measure fractal dimension of grid."""
    width = grid.width()
    height = grid.height()
    grid = np.array(grid._grid) == 0

    counts = []
    ruler = 1
    while (ruler < width) and (ruler < height):
        count = 0
        for x in range(width // ruler):
            for y in range(height // ruler):
                count = count + grid[
                    (x * ruler):((x + 1) * ruler),
                    (y * ruler):((y + 1) * ruler)
                ].any()
        counts.append((ruler, count))
        ruler *= 2

    return counts


def print_grid(grid, seed, details="full"):
    """Show the result."""
    print(grid.width(), grid.height(), grid.depth(), seed)
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
