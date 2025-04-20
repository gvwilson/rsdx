import random
from unittest.mock import patch
from grid import Grid, fill_grid


def test_exact_grid():
    fixture = Grid(5)
    moves = [[-1, 0], [1, 0], [-1, 0], [1, 0], [0, 1], [0, 1], [0, 1]]
    with patch("random.choice", side_effect=moves):
        num = fill_grid(fixture)
    assert num == 6
    assert str(fixture).strip().split("\r\n") == [
        "0,0,0,0,0",
        "0,0,2,0,0",
        "0,0,3,1,0",
        "0,0,0,0,0",
        "0,0,0,0,0",
    ]
