# The Grid

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

[`grid_01.py`](./grid_01.py)

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

[`grid_02.py`](./grid_02.py)

-   Operation is in a function that we can call from other code
-   [Seed](g:seed) the random number generator for reproducibility
-   Use a [list comprehension](g:list_comprehension) to create the grid
    -   Could shorten the code further with a [nested comprehension](g:nested_comprehension)
-   Use a condition in the `while` loop instead of `break`
-   But data representation still shows through

## Use a Class

[`grid_03.py`](./grid_03.py)

-   Hide data representation in a class
    -   Exercise: replace list of lists with NumPy array
-   Provide [getter](s:getter) and [setter](s:setter) methods
-   `fill` is a separate function
    -   `Grid` class might be used for other things
-   Use [string I/O](g:string_io) to build CSV representation

## Command-Line Parameters

[`grid_04.py`](./grid_04.py)

-   Use `argparse` module to turn command-line arguments into an object with named values
-   Saves us from mixing up seeds and sizes
-   Makes [shell scripts](g:shell_script) easier to read
-   And gives us a `--help` option that's guaranteed to be up to date
