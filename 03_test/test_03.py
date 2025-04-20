import random
from unittest.mock import patch
from grid import Grid, fill_grid


def test_move_in_one_direction():
    fixture = Grid(5)
    with patch("random.choice", return_value=[-1, 0]):
        fill_grid(fixture)
    expected = {(1, 2), (2, 2)}
    for x in range(5):
        for y in range(5):
            if (x, y) in expected:
                assert fixture[x, y] == 1
            else:
                assert fixture[x, y] == 0
