# Testing

## The Problem

-   How can we tell if our grid filler is working correctly?
-   Particularly since filling it is random

## First Test

-   Border should always be zero

```{data-file="test_01.py"}
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
```

-   But that's just one possible grid

## Parameterize Tests

```{data-file="test_02.py"}
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
```

-   A [parameterized test](g:parameterize_test) runs once for each parameter value
-   So it's better, but there are still a lot of other possible grids

## Force a Grid

```{data-file="test_03.py"}
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
```

-   [Patch](g:patch) `random.choice` so that it always returns `[-1, 0]`
-   Figure out what the values should be and check them
    -   Implicitly checks that filling stops at the boundary

## Counting

-   Total of grid values should be the number of moves
-   So modify `fill_grid` to return that

```{data-file="test_04.py"}
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
```

## Force Filling the Whole Grid

```{data-file="test_05.py"}
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
```

-   `csv.writer` uses Windows line endings
-   So strip off the last one and split to compare

## Statistical Properties

```{data-file="test_06.py"}
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

    assert ave_num == pytest.approx(size ** 2 / 4, rel=0.2)
    with pytest.raises(AssertionError):
        assert ave_center == pytest.approx(1 + math.pi / math.log(size), rel=0.2)
```

-   Unsatisfying
-   Math tells us what the average number of steps should be,
    but it takes a long time (on a large grid) to get close to that
    -   Try adjusting the seed, the size, etc.
-   Average number of visits to center with absorbing boundary condition is even less satisfying
