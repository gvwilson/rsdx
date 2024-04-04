---
title: "Refactor"
tagline: "Refactor a student-quality script that models the spread of pollution."
syllabus:
-   Break code into comprehensible chunks.
-   Create classes and class hierarchies.
-   Write docstrings and generating documentation pages.
-   Validate implementations against one another.
---

-   Goal is to refactor a program that (kind of) works
    to create something we can do more work with
-   Original problem is [%g inv_perc "invasion percolation" %]
    -   Grid of random numbers
    -   Fill the center cell
    -   Repeatedly:
        -   Find the cell adjacent to the filled region with the lowest value
	-   Fill it
    -   Until we reach the edge
-   Models spread of pollutant through fractured rock (among other things)

## Original Script {: #refactor-original}

-   Main body of code
    -   Always need width, height and depth (range of random integer values)
    -   [%g rng_seed "Random number seed" %] is optional

[%inc script.py mark=main %]

-   Make a grid as a list of lists
    -   Has a docstring

[%inc script.py pattern=func:make_grid %]

-   Choose the next cell to fill in by sweeping the whole grid

[%inc script.py pattern=func:choose_cell %]

-   Relies on another function to test adjacency

[%inc script.py pattern=func:adjacent %]

-   We also need to test if we're on the border

[%inc script.py pattern=func:on_border %]

-   And finally, show the result

[%inc script.py pattern=func:print_grid %]

## Critique {: #refactor-critique}

-   What if we want to change the way the grid is implemented?
-   Or the way we search for the next cell to fill?
-   Most meaningful test of software design quality is "how easy is it to make a plausible change?"

## A Generic Driver {: #refactor-generic}

-   Main function

[%inc invperc.py pattern=func:main %]

-   Relies on a setup function
    -  Can easily replace this in future with something that reads parameters from a file

[%inc invperc.py pattern=func:setup %]

-   We're going to build (at least) two grid classes, so import both here

[%inc invperc.py mark=import %]

-   Initialization relies on the grid's constructor
    -   All grids take the same parameters in the same order

[%inc invperc.py pattern=func:initialize_grid %]

-   Keep printing here
    -   Could have grids print themselves

[%inc invperc.py pattern=func:print_grid %]

## Three Kinds of Grid {: #refactor-concrete}

-   First grid is an [%g abc "abstract base class" %]
    -   Defines common behaviors
    -   Requires derived classes to provide a way to get and set item by location

[%inc grid_generic.py mark=main %]

-   Other operations defined in terms of the common methods
    -   Including the ones the derived classes have to implement
-   Filling

[%inc grid_generic.py pattern="class:GridGeneric meth:fill" %]

-   Choose the next cell:

[%inc grid_generic.py pattern="class:GridGeneric meth:choose_cell" %]

-   Adjacency test

[%inc grid_generic.py pattern="class:GridGeneric meth:adjacent" %]

-   Border test

[%inc grid_generic.py pattern="class:GridGeneric meth:on_border" %]

-   Now implement a grid that uses list-of-lists like before

[%inc grid_list.py pattern="class:GridList" %]

-   And another that uses a NumPy array

[%inc grid_array.py pattern="class:GridArray" %]

-   Should always get identical answer regardless of which grid is used
    -   For the same parameters including RNG seed of course
-   Allows cross-validation of implementations
