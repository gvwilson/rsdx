import random
from grid import Grid, fill_grid


def test_edges_unfilled():
    random.seed(12345)
    fixture = Grid(5)
    fill_grid(fixture)
    for p in (0, 4):
        for q in range(5):
            assert fixture[p, q] == 0
            assert fixture[q, p] == 0
