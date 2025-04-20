import math
import random
import pytest
from grid import Grid, fill_grid


def test_statistical_properties():
    random.seed(12345)
    num_trials = 500
    size = 301

    center = size // 2
    total_num = 0
    total_center = 0

    for _ in range(num_trials):
        fixture = Grid(size)
        total_num += fill_grid(fixture)
        total_center += fixture[center, center]

    ave_num = total_num / num_trials
    ave_center = total_center / num_trials

    assert ave_num == pytest.approx(size**2 / 4, rel=0.2)
    with pytest.raises(AssertionError):
        assert ave_center == pytest.approx(1 + math.pi / math.log(size), rel=0.2)
