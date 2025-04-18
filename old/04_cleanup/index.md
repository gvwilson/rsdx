# Cleaning Up Code

## The Problem

-   Refactor and test a program that (kind of) works to create something sturdier
-   Program models [invasion percolation](g:inv_perc)
    -   Grid of random numbers
    -   Fill the center cell
    -   Repeatedly:
        -   Find the cell adjacent to the filled region with the lowest value
	-   Fill it
    -   Until we reach the edge
-   Models spread of pollutant through fractured rock (among other things)

---

## Main Body of Original Script

-   Note: [random number seed](g:rng_seed) is optional

```{data-file="script.py:main"}
# Grid size and range of fill values.
width, height, depth = (int(x) for x in sys.argv[1:4])

# Random number generation.
seed = int(sys.argv[4]) if len(sys.argv) > 4 else randrange(sys.maxsize)
randseed(seed)

# Create initial grid
grid = make_grid(width, height, depth)

# Fill central cell.
grid[width // 2][height // 2] = 0

# Fill other cells.
while True:
    x, y = choose_cell(grid)
    grid[x][y] = 0
    if on_border(width, height, x, y):
        break

# Show result.
print_grid(grid, width, height, depth, seed)
```

---

## The Grid

-   Make a grid as a list of lists
    -   Has a docstring

```{data-file="script.py:make_grid"}
def make_grid(width, height, depth):
    """Create a width X height grid."""
    grid = []
    for x in range(width):
        row = []
        for y in range(height):
            row.append(randint(1, depth))
        grid.append(row)
    return grid
```

---

## Choosing the Next Cell

-   Sweep the whole grid

```{data-file="script.py:choose_cell"}
def choose_cell(grid):
    """Choose the next cell to fill in."""
    least, cx, cy = None, None, None
    for x in range(len(grid)):
        row = grid[x]
        for y in range(len(row)):
            temp = grid[x][y]
            if not adjacent(grid, x, y):
                continue
            if (least is None) or ((temp != 0) and (temp < least)):
                least, cx, cy = temp, x, y
    return cx, cy
```

---

## Helper Functions

-   Test adjacency

```{data-file="script.py:adjacent"}
def adjacent(grid, x, y):
    """Is (x, y) adjacent to a filled cell?"""
    x_1, y_1 = x + 1, y + 1
    if (x > 0) and (grid[x - 1][y] == 0):
        return True
    if (x_1 < len(grid)) and (grid[x_1][y] == 0):
        return True
    if (y > 0) and (grid[x][y - 1] == 0):
        return True
    if (y_1 < len(grid[x])) and (grid[x][y_1] == 0):
        return True
    return False
```

---

## Helper Functions

-   We also need to test if we're on the border

```{data-file="script.py:on_border"}
def on_border(width, height, x, y):
    """Is this cell on the border of the grid?"""
    if (x == 0) or (x == width - 1):
        return True
    if (y == 0) or (y == height - 1):
        return True
    return False
```

---

## Display

-   And finally, show the result

```{data-file="script.py:print_grid"}
def print_grid(grid, width, height, depth, seed, as_numbers=False):
    """Show the result."""
    print(width, height, depth, seed)
    height = len(grid[0])
    for y in range(height - 1, -1, -1):
        for x in range(len(grid)):
            if as_numbers:
                sys.stdout.write(f"{grid[x][y]:02d} ")
            else:
                sys.stdout.write("X" if grid[x][y] == 0 else ".")
        sys.stdout.write("\n")
```

---

## Critique

-   What if we want to change the way the grid is implemented?
-   Or the way we search for the next cell to fill?
-   Most meaningful measure of the quality of software design is,
    "How easy is it to make a plausible change?"

---

## A Generic Driver

-   Main function

```{data-file="invperc.py:main"}
def main():
    """Main driver."""
    kind, width, height, depth, seed = setup()
    grid = initialize_grid(kind, width, height, depth)
    grid.fill()
    print_grid(kind, grid, seed)
```

---

## Setting Up

-   Relies on a setup function
    -  Can easily replace this in future with something that reads parameters from a file

```{data-file="invperc.py:setup"}
def setup():
    """Get parameters."""
    kind = sys.argv[1]
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    depth = int(sys.argv[4])

    if len(sys.argv) > 5:
        seed = int(sys.argv[5])
    else:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)

    return kind, width, height, depth, seed
```

---

## Refactoring

-   We're going to build (at least) two grid classes, so import both here

```{data-file="invperc.py:import"}
from grid_list import GridList
from grid_array import GridArray
```

-   Initialization relies on the grid's constructor
    -   All grids take the same parameters in the same order

```{data-file="invperc.py:initialize_grid"}
def initialize_grid(kind, width, height, depth):
    """Prepare grid for simulation."""
    lookup = {
        "list": GridList,
        "array": GridArray,
    }
    return lookup[kind](width, height, depth)
```

---

## Printing

-   Keep printing here
    -   Could have grids print themselves

```{data-file="invperc.py:print_grid"}
def print_grid(kind, grid, seed, details="full"):
    """Show the result."""
    print(kind, grid.width(), grid.height(), grid.depth(), seed)
    if details == "brief":
        return
    for y in range(grid.height() - 1, -1, -1):
        for x in range(grid.width()):
            if details == "numbers":
                sys.stdout.write(f"{grid[x, y]:02d} ")
            else:
                sys.stdout.write("X" if grid[x, y] == 0 else ".")
        sys.stdout.write("\n")
```

---

## Generic Grids

-   First grid is an [abstract base class](g:abc)
    -   Defines common behaviors
    -   Declaring [abstract methods](g:abstract_method)
        forces derived classes to provide a way to get and set item by location

```{data-file="grid_generic.py:main"}
from abc import ABC, abstractmethod

class GridGeneric(ABC):
    """Represent a generic grid."""

    @abstractmethod
    def __getitem__(self, key):
        """Get value at location."""

    @abstractmethod
    def __setitem__(self, key, value):
        """Set value at location."""

    def __init__(self, width, height, depth):
        """Record shared state."""
        self._width = width
        self._height = height
        self._depth = depth
```

---

## Other Methods

-   All other operations rely on these abstract methods
    -   Including the ones the derived classes have to implement
-   E.g. filling

```{data-file="grid_generic.py:fill"}
    def fill(self):
        """Fill grid one cell at a time."""
        self[self.width() // 2, self.height() // 2] = 0
        while True:
            x, y = self.choose_cell()
            self[x, y] = 0
            if self.on_border(x, y):
                break
    ```

---

## Injecting What We Need

-   Create a new class `GridListRandomizer` that takes a number generator as a constructor parameter
    -   Generate a grid filled with known values for testing

```{data-file="grid_list_randomizer.py:init"}
    def __init__(self, width, height, depth, rand=random.randint):
        """Construct and fill."""
        super().__init__(width, height, depth)
        self._rand = rand
        self._grid = []
        for x in range(self._width):
            row = []
            for y in range(self._height):
                row.append(self._rand(1, depth))
            self._grid.append(row)
    ```

---

## A Testable Grid

-   `grid_filled.py` defines `GridFilled`, which we can populate with whatever data we want

```{data-file="grid_filled.py:init"}
    def __init__(self, width, height, depth, values):
        """Construct and fill."""
        assert len(values) == width
        assert all(len(col) == height for col in values)
        super().__init__(width, height, depth)
        self._grid = [col[:] for col in values]
    ```

---

## Oops

-   But suddenly realize: what happens when several fillable cells have the same value?
    -   `fill_grid` always chooses the first one it encounters in this case
    -   So filling has a bias toward the (0,0) corner of the grid
-   [The next chapter](../05_perf/index.md) will tackle this problem
-   But first, let's see how fast our code is…

---

## Exercises

1.  Refactor grid classes so that we have a patchable method for filling initial values.
