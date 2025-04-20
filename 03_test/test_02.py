import random
import pytest
from grid import Grid, fill_grid


@pytest.mark.parametrize("seed", [123, 1234, 12345, 123456, 1234567])
def test_edges_unfilled(seed):
    random.seed(seed)
    fixture = Grid(5)
    fill_grid(fixture)
    for p in (0, 4):
        for q in range(5):
            assert fixture[p, q] == 0
            assert fixture[q, p] == 0
