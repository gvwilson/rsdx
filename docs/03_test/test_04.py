import random
import pytest
from grid import Grid, fill_grid


@pytest.mark.parametrize("seed", [123, 1234, 12345, 123456, 1234567])
def test_sum_cell_values(seed):
    fixture = Grid(5)
    expected = fill_grid(fixture)
    actual = 0
    for x in range(5):
        for y in range(5):
            actual += fixture[x, y]
    assert expected == actual
