"""Invasion percolation in Python."""

import argparse
import random
import sys

from grid import Grid


def initialize_random(seed=None):
    """Initialize RNG in reproducible way."""
    if seed is None:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    return seed


def percolate(args):
    """Run all simulations."""
    initialize_random(args.seed)
    grid = Grid(args.size, args.size, args.depth)
    grid.fill()
    return grid


if __name__ == "__main__":

    def main():
        """Main driver."""
        args = parse_args()
        result = percolate(args)
        print(result)

    def parse_args():
        """Get command-line parameters."""
        parser = argparse.ArgumentParser()
        parser.add_argument("--depth", type=int, default=2, help="depth")
        parser.add_argument("--details", type=str, default=None, help="output file")
        parser.add_argument("--size", type=int, default=3, help="size")
        parser.add_argument("--reps", type=int, default=1, help="repetitions")
        parser.add_argument("--seed", type=int, default=None, help="RNG seed")
        return parser.parse_args()
