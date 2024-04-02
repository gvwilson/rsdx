---
title: "A Lazy Algorithm"
tagline: "Create a lazy implementation of invasion percolation that's much faster."
syllabus:
-   Estimating algorithm performance with big-oh.
-   Extending a class hierarchy to accommodate new features.
-   Adapting tools written earlier to make all of this simpler to run, test, and document.
---

-   Start with the punchline and work backward
-   The bottom lines in this graph show the performance we can get by changing our implementation of invasion percolation

[% figure
   slug="lazy_example"
   img="./k+lazy+list+array_z+35+55+75+95+115_d+2+10+100_r+50_s+556677.svg"
   caption="Running times for various depths and sizes."
   alt="Line graph showing that the lazy algorithm's performance is nearly flat."
%]

## Lazy Evaluation {: #lazy-eval}

-   We have been searching the entire grid to find the next cell to fill
    -   But we only need to look on the border
    -   And we can keep track of where the border is
-   Keep a dictionary called `candidates`
    -   Key: a value in the grid
    -   Values: coordinates of cells on the border that have that value
-   On each step:
    -   Find the lowest key
    -   Choose one of its cells at random (to solve the bias problem discovered earlier)
    -   Fill it in
    -   Add its unfilled neighbors to `candidates`
-   Trading space for time
    -   Storing cell values and coordinates is redundant
    -   But filling the next cell now takes constant time regardless of grid size
-   `GridLazy` constructor

[%inc grid_lazy.py pattern="class:GridLazy meth:__init__" %]

-   Filling algorithm overrides inherited method
    -   Fill the center cell
    -   Add its neighbors as candidates
    -   Repeatedly choose a cell to fill (stopping if we've reached the boundary)

[%inc grid_lazy.py pattern="class:GridLazy meth:fill" %]

-   Adding candidates

[%inc grid_lazy.py pattern="class:GridLazy meth:add_candidates" %]
[%inc grid_lazy.py pattern="class:GridLazy meth:add_one_candidate" %]

-   Choosing a cell

[%inc grid_lazy.py pattern="class:GridLazy meth:choose_cell" %]

-   Sweep the same parameter ranges as before
-   Performance is much better
    -   Searching an \\( N{\times}N \\) grid is \\( N^2 \\) operations
    -   Fill about \\( N^{1.5} \\) cells (it's a fractal)
    -   So running time of the naïve approach is proportional to \\( N^{3.5} \\)
    -   Which a computer scientist would write \\( \mathcal{O}(N^{3.5}) \\)
    -   Running time of lazy approach is just \\( \mathcal{O}(N^{1.5}) \\)

## Testing {: #lazy-test}

[%fixme "show how to test lazy approach with randomnmess" %]

## Exercises {: #lazy-exercises}

1.  Modify the list and array implementation to collect candidate cells of equal lowest value
    and select one of those.

1.  Does it make sense to pre-populate `candidates` by adding *all* cells in the grid
    at the start of the program?
    Why or why not?
