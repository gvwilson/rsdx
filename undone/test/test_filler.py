"""Test grid operations."""

import pytest
from unittest.mock import patch

from grid import Grid
from filler import Filler


@pytest.fixture
def small():
    return Filler(Grid(5, 5, 2, [[2] * 5] * 5))


def test_fill_first_cell(small):
    small.fill_first_cell()
    for x, y, val in small.grid().sweep():
        if (x == 2) and (y == 2):
            assert small.grid()[x, y] == Grid.FILLED
        else:
            assert small.grid()[x, y] == 2


def test_choose_correct_cell_only_one(small):
    small.grid()[1, 2] = 1
    small.fill_first_cell()
    assert small.choose_cell() == (1, 2)


def test_choose_correct_cell_among_two(small):
    small.grid()[1, 2] = 1
    small.grid()[3, 2] = 1
    small.fill_first_cell()
    with patch("random.choice", lambda x: x[-1]):
        assert small.choose_cell() == (3, 2)


def test_choose_correct_cell_with_distractors(small):
    small.grid()[1, 2] = 1
    small.grid()[3, 2] = 1
    small.grid()[3, 3] = 1
    small.fill_first_cell()
    with patch("random.choice", lambda x: x[-1]):
        assert small.choose_cell() == (3, 2)


def test_fill_to_edge(small):
    small.grid()[3, 2] = 1
    small.grid()[4, 2] = 1
    small.fill(randomize=False)
    assert small.grid() == Grid(
        5,
        5,
        2,
        [
            [2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2],
            [2, 2, 0, 2, 2],
            [2, 2, 0, 2, 2],
            [2, 2, 0, 2, 2],
        ],
    )
