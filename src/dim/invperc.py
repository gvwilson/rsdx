"""Invasion percolation in Python."""

import argparse
import random
import numpy as np
import pandas as pd
from pathlib import Path
import sys

from grid import Grid


def main():
    """Main driver."""
    args = setup()
    initialize_random(args.seed)
    results = percolate(args)
    dim = -np.polyfit(np.log(results["ruler"]), np.log(results["count"]), 1)[0]
    print(dim)
    if args.details:
        Path(args.details).write_text(results.to_csv(index=False))


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
    """Initialize RNG in reproducible way."""
    if seed is None:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    return seed


def percolate(args):
    """Run all simulations."""
    result = []
    for _ in range(args.reps):
        seed = initialize_random()
        grid = Grid(args.size, args.size, args.depth)
        grid.fill()
        dims = measure_dimension(grid)
        result.extend([(args.size, args.depth, seed, *d) for d in dims])
    return pd.DataFrame(result, columns=("size", "depth", "seed", "ruler", "count"))


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
                count = (
                    count
                    + grid[
                        (x * ruler) : ((x + 1) * ruler), (y * ruler) : ((y + 1) * ruler)
                    ].any()
                )
        counts.append((ruler, count))
        ruler *= 2

    return counts


if __name__ == "__main__":
    main()
