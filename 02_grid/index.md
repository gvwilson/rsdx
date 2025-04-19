# Making Grids

## The Problem

-   First step in synthesizing data is to model spread of pollution
    -   Doesn't *have* to first, but we have to start somewhere…
-   Factors
    -   Survey areas will be marked off in meter-by-meter squares,
        so we can use a discrete grid
    -   Survey grids are anywhere from 8x8 to 100x100 meters
        -   Not guaranteed to be square, but all the old grids were
    -   Pollution spreads from a central point,
        so we want connected regions
    -   Pollution decreases with distance from the dumping site,
        but may pool in low-lying or porous areas

## The Plan

-   Throw together something simple and then [refactor](g:refactor) it
    -   Creates opportunities to explain why we do things certain ways
    -   It's how most of us build software in real life

## The First Version

```{data-file="grid_01.py"}
import random

size = 11  # change this to make a larger grid

# Make an empty grid
grid = []
for i in range(size):
    temp = []
    for j in range(size):
        temp.append(0)
    grid.append(temp)

center = size // 2  # remember to do integer division
x, y = center, center

# Move and fill until we reach the edge
moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
while True:
    grid[x][y] += 1
    m = random.choice(moves)
    x += m[0]
    y += m[1]
    if (x == 0) or (y == 0):
        break
    if (x == size - 1) or (y == size - 1):
        break

# Print as CSV
for y in range(size):
    for x in range(size):
        print(grid[x][y], end="")
        if x < size - 1:
            print(",", end="")
    print()
```

-   Store the grid as a list of lists
    -   Could use [NumPy][numpy] array
-   Use a [random walk](g:random_walk) to set cells' values
    -   Add one to the cell each time the walker visits it
    -   Produces 2D normal distribution in the limit
-   Store a list of possibly moves
-   Repeatedly select one at random
-   Stop when the walker reaches the edge of the grid
-   Print as [CSV](g:csv)

## Critique

-   Everything is [coupled](g:coupling) to the grid representation
    -   If we *did* switch to a NumPy array,
        we'd have to rewrite all the low-level details
-   Not [reproducible](g:reproducibility)
    -   Different sequence of random numbers each time we run it
-   Have to edit the script to change the grid size
-   Result is printed to the screen
    -   We can redirect to a file using `>` in the shell

## Tidying Up

```{data-file="grid_02.py"}
import csv
import random
import sys


def make_grid(size):
    """Create and fill a square of the specified size."""

    # Make an empty grid
    grid = []
    for i in range(size):
        grid.append([0 for _ in range(size)])

    # Prep
    center = size // 2
    size_1 = size - 1
    moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]

    # Move and fill until we reach the edge
    x, y = center, center
    while (x != 0) and (y != 0) and (x != size_1) and (y != size_1):
        grid[x][y] += 1
        m = random.choice(moves)
        x += m[0]
        y += m[1]

    return grid


if __name__ == "__main__":
    size = int(sys.argv[1])
    seed = int(sys.argv[2])
    random.seed(seed)
    grid = make_grid(size)
    csv.writer(sys.stdout).writerows(grid)
```

-   Operation is in a function that we can call from other code
-   [Seed](g:seed) the random number generator for reproducibility
-   Use a [list comprehension](g:list_comprehension) to create the grid
    -   Could shorten the code further with a [nested comprehension](g:nested_comprehension)
-   Use a condition in the `while` loop instead of `break`
-   But data representation still shows through

## Use a Class

```{data-file="grid_03.py"}
import csv
import io
import random
import sys


class Grid:
    """Store a grid of numbers."""

    def __init__(self, size):
        """Construct empty grid."""
        assert size > 0, f"Grid size must be positive not {size}"
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]

    def __getitem__(self, key):
        """Get grid element."""
        x, y = key
        return self.grid[x][y]

    def __setitem__(self, key, value):
        """Set grid element."""
        x, y = key
        self.grid[x][y] = value

    def __str__(self):
        """Convert to string."""
        output = io.StringIO()
        csv.writer(output).writerows(self.grid)
        return output.getvalue()


def fill_grid(grid):
    """Fill in a grid."""

    moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    center = grid.size // 2
    size_1 = grid.size - 1
    x, y = center, center
    while (x != 0) and (y != 0) and (x != size_1) and (y != size_1):
        grid[x, y] += 1
        m = random.choice(moves)
        x += m[0]
        y += m[1]


if __name__ == "__main__":
    size = int(sys.argv[1])
    seed = int(sys.argv[2])
    random.seed(seed)
    grid = Grid(size)
    fill_grid(grid)
    print(grid)
```

-   Hide data representation in a class
    -   Exercise: replace list of lists with NumPy array
-   Provide [getter](g:getter) and [setter](g:setter) methods
-   `fill` is a separate function
    -   `Grid` class might be used for other things
-   Use [string I/O](g:string_io) to build CSV representation

## Command-Line Parameters

```{data-file="grid_04.py"}
import argparse
import csv
import io
import random


class Grid:
    """Store a grid of numbers."""

    def __init__(self, size):
        """Construct empty grid."""
        assert size > 0, f"Grid size must be positive not {size}"
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]

    def __getitem__(self, key):
        """Get grid element."""
        x, y = key
        return self.grid[x][y]

    def __setitem__(self, key, value):
        """Set grid element."""
        x, y = key
        self.grid[x][y] = value

    def __str__(self):
        """Convert to string."""
        output = io.StringIO()
        csv.writer(output).writerows(self.grid)
        return output.getvalue()


def cmdline_args():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, required=True, help="RNG seed")
    parser.add_argument("--size", type=int, required=True, help="grid size")
    return parser.parse_args()


def fill_grid(grid):
    """Fill in a grid."""

    moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    center = grid.size // 2
    size_1 = grid.size - 1
    x, y = center, center
    while (x != 0) and (y != 0) and (x != size_1) and (y != size_1):
        grid[x, y] += 1
        m = random.choice(moves)
        x += m[0]
        y += m[1]


if __name__ == "__main__":
    args = cmdline_args()
    random.seed(args.seed)
    grid = Grid(args.size)
    fill_grid(grid)
    print(grid)
```

-   Use `argparse` module to turn command-line arguments into an object with named values
-   Saves us from mixing up seeds and sizes
-   Makes [shell scripts](g:shell_script) easier to read
-   And gives us a `--help` option that's guaranteed to be up to date
