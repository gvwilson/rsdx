"""Invasion percolation in Python."""

import argparse
import random
import pandas as pd
import sys
import time

from grid import GridNestedList, GridArray
from lazy import GridLazy


# Known kinds of grids.
KINDS = {
    "list": GridNestedList,
    "array": GridArray,
    "lazy": GridLazy,
}

def main():
    """Main driver."""
    args = setup()
    all_seeds = [random.randrange(sys.maxsize) for _ in range(args.reps)]
    results = run_all(args, all_seeds)
    if args.details:
        print(results)
    print(results[["kind", "time"]].groupby("kind").agg(func="mean").to_csv())


def setup():
    """Get parameters."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", type=int, default=2, help="depth")
    parser.add_argument("--details", action="store_true", default=False, help="show details")
    parser.add_argument("--height", type=int, default=3, help="height")
    parser.add_argument("--reps", type=int, default=1, help="repetitions")
    parser.add_argument("--seed", type=int, default=None, help="RNG seed")
    parser.add_argument("--width", type=int, default=3, help="width")
    args = parser.parse_args()

    if args.seed is None:
        args.seed = random.randrange(sys.maxsize)
    random.seed(args.seed)

    return args


def run_all(args, all_seeds):
    results = pd.DataFrame(columns=("kind", "width", "height", "depth", "seed", "time"))
    for seed in all_seeds:
        all_grids = {}
        for kind in KINDS.keys():
            random.seed(seed)
            grid = initialize_grid(kind, args.width, args.height, args.depth)
            t_start = time.time()
            fill_grid(grid)
            t_elapsed = time.time() - t_start
            results.loc[len(results)] = (kind, args.width, args.height, args.depth, seed, t_elapsed)
            all_grids[kind] = grid
        check_equal(all_grids)
    return results


def initialize_grid(kind, width, height, depth):
    """Prepare grid for simulation."""
    return KINDS[kind](width, height, depth)


def fill_grid(grid):
    """Fill grid one cell at a time."""
    grid.fill_first_cell()
    while True:
        x, y = grid.choose_cell()
        grid[x, y] = 0
        if grid.on_border(x, y):
            break


def check_equal(all_grids):
    """Check that all grids got the same answer."""
    kinds = list(KINDS.keys())
    reference = all_grids[kinds[0]]
    for other_kind in kinds[1:]:
        if all_grids[other_kind] != reference:
            print(f"{other_kind} != {kinds[0]}")


def print_grid(grid, seed, details="full"):
    """Show the result."""
    print(grid.width(), grid.height(), grid.depth(), seed)
    if (details == "brief"):
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
