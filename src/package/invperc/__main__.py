"""Entry point for command-line execution."""

import argparse
import json
import random
import sys

from . import invperc

DEPTH = 10  # default range of random values in grid
HEIGHT = 15  # default Y dimension of grid
WIDTH = 15  # default X dimension of grid


def main():
    """Main command-line driver for invasion percolation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", type=int, default=DEPTH, help="random depth")
    parser.add_argument("--height", type=int, default=HEIGHT, help="grid height")
    parser.add_argument("--seed", type=int, required=True, help="RNG seed")
    parser.add_argument("--width", type=int, default=WIDTH, help="grid width")
    args = parser.parse_args()

    random.seed(args.seed)
    grid = invperc(args.width, args.height, args.depth)
    print(grid)

    return 0


if __name__ == "__main__":
    main()
