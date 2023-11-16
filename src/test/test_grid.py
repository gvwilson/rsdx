"""Test grid operations."""

import pytest

from grid import Grid


def test_initially_uninitialized():
    g = Grid(2, 3, 4)
    assert g.width() == 2
    assert g.height() == 3
    assert g.depth() == 4
    for x, y, _ in g.sweep():
        with pytest.raises(AssertionError):
            g[x, y]


def test_set_individual_values():
    g = Grid(2, 3, 4)
    for x, y, _ in g.sweep():
        g[x, y] = 1 + ((x + y) % 4)
    for y in range(g.height()):
        for x in range(g.width()):
            assert g[x, y] == 1 + ((x + y) % 4)


def test_set_all_values_when_constructing():
    values = [[1, 1, 1], [2, 2, 2]]
    g = Grid(2, 3, 4, values)
    assert all(g[0, y] == 1 for y in range(g.height()))
    assert all(g[1, y] == 2 for y in range(g.height()))
