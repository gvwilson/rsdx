"""Invasion percolation interface."""

from .grid import Grid


def invperc(width, height, depth):
    """Simulate invasion percolation on a grid.

    Creates a width X height grid with integer random values in the
    range 1..depth inclusive, fills from the center, and returns the
    resulting `Grid` object. Note that this function does *not*
    seed Python's `random` module.

    Args:
        width: X size of grid (positive integer).
        height: Y size of grid (positive integer).
        depth: range of random grid values (positive integer).

    Returns:
        A filled instance of `Grid`.
    """
    grid = Grid(width, height, depth)
    grid.fill()
    return grid
