"""Invasion percolation in Python."""

import argparse
from collections import defaultdict
import pandas as pd
from pathlib import Path
import random
import sys

from filler import Filler
from grid import Grid


def main():
    """Main driver."""
    args = setup()
    seed = initialize_random(args.seed)
    runs, results = percolate(args)
    if args.save:
        stem = f"{args.size}_{args.depth}_{args.reps}_{seed}"
        Path(f"runs_{stem}.csv", "w").write_text(runs.to_csv(index=False))
        Path(f"results_{stem}.csv", "w").write_text(results.to_csv(index=False))
    else:
        print(results.to_csv(index=False))


def setup():
    """Get parameters."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", type=int, default=2, help="depth")
    parser.add_argument("--size", type=int, default=3, help="size")
    parser.add_argument("--reps", type=int, default=1, help="repetitions")
    parser.add_argument(
        "--save", action="store_true", default=False, help="save to file"
    )
    parser.add_argument("--seed", type=int, default=None, help="RNG seed")
    parser.add_argument(
        "--verbose", action="store_true", default=False, help="report progress"
    )
    args = parser.parse_args()
    args.width = args.height = args.size
    return args


def initialize_random(seed=None):
    """Initialize RNG in reproducible way."""
    if seed is None:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    return seed


def percolate(args):
    """Run all simulations."""
    runs = []
    results = []
    for i in range(args.reps):
        if args.verbose:
            print(f"...{i}")
        seed = initialize_random()
        filler = Filler(Grid(args.width, args.height, args.depth))
        filler.fill()
        density = calculate_density(filler.grid())
        runs.append((i, args.size, args.depth, seed))
        results.extend([(i, distance, fraction) for (distance, fraction) in density])
    runs = pd.DataFrame(runs, columns=("id", "size", "depth", "seed"))
    results = pd.DataFrame(results, columns=("id", "distance_2", "fraction"))
    return runs, results


def calculate_density(grid):
    """Calculate density versus distance from center of grid."""
    cx, cy = grid.width() // 2, grid.height() // 2
    count_cells = defaultdict(int)
    count_filled = defaultdict(int)
    for x, y, val in grid.sweep():
        dist_2 = (x - cx) ** 2 + (y - cy) ** 2
        count_cells[dist_2] += 1
        if val == grid.FILLED:
            count_filled[dist_2] += 1

    result = [
        (dist_2, count_filled[dist_2] / count_cells[dist_2])
        for dist_2 in sorted(count_cells.keys())
    ]
    return result


if __name__ == "__main__":
    main()
