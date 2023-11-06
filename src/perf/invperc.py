"""Invasion percolation in Python."""

import argparse
import random
import pandas as pd
import sys
import time

from grid_list import GridList
from grid_array import GridArray


# Known kinds of grids.
KINDS = {
    "list": GridList,
    "array": GridArray,
}


def main():
    """Main driver."""
    args = setup()
    all_seeds = [random.randrange(sys.maxsize) for _ in range(args.reps)]
    results = run_all(args, all_seeds)
    if args.details:
        with open(args.details, "w") as writer:
            print(results.to_csv(index=False), file=writer)
    print(results[["kind", "time"]].groupby("kind").agg(func="mean").to_csv())


def setup():
    """Get parameters."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", type=int, default=2, help="depth")
    parser.add_argument("--details", type=str, default=None, help="output file")
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
    """Run all variations."""
    results = pd.DataFrame(columns=("kind", "width", "height", "depth", "seed", "time"))
    for seed in all_seeds:
        all_grids = {}
        for kind in KINDS.keys():
            random.seed(seed)
            grid = initialize_grid(kind, args.width, args.height, args.depth)
            t_start = time.time()
            fill_grid(grid)
            t_elapsed = time.time() - t_start
            results.loc[len(results)] = (
                kind,
                args.width,
                args.height,
                args.depth,
                seed,
                t_elapsed,
            )
            all_grids[kind] = grid
        check_equal(all_grids)
    return results


def initialize_grid(kind, width, height, depth):
    """Prepare grid for simulation."""
    return KINDS[kind](width, height, depth)


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
            if temp == 0:
                continue
            if not grid.adjacent(x, y):
                continue
            if (least is None) or (temp < least):
                least, cx, cy = temp, x, y
    return cx, cy


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
