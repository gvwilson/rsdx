"""Invasion percolation in Python."""

from invperc_util import *
from params_single import ParamsSingle


def main():
    """Main driver."""
    params = setup(ParamsSingle)
    initialize_random(params)
    grid = initialize_grid(params)
    num_filled = fill_grid(grid)
    if len(sys.argv) > 2:
        print_grid(params, grid, num_filled, details="full")


if __name__ == "__main__":
    main()
