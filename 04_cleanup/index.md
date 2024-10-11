# Cleanup

## The Problem

-   Refactor and test a program that (kind of) works to create something sturdier
-   Program models [invasion](g:inv_perc)colation" %]
    -   Grid of random numbers
    -   Fill the center cell
    -   Repeatedly:
        -   Find the cell adjacent to the filled region with the lowest value
	-   Fill it
    -   Until we reach the edge
-   Models spread of pollutant through fractured rock (among other things)

---

## Main Body of Original Script

-   Note: [random](g:rng_seed)ber seed" %] is optional

[%inc script.py keep=main %]

---

## The Grid

-   Make a grid as a list of lists
    -   Has a docstring

[%inc script.py keep=make_grid %]

---

## Choosing the Next Cell

-   Sweep the whole grid

[%inc script.py keep=choose_cell %]

---

## Helper Functions

-   Test adjacency

[%inc script.py keep=adjacent %]

---

## Helper Functions

-   We also need to test if we're on the border

[%inc script.py keep=on_border %]

---

## Display

-   And finally, show the result

[%inc script.py keep=print_grid %]

---

## Critique

-   What if we want to change the way the grid is implemented?
-   Or the way we search for the next cell to fill?
-   Most meaningful measure of the quality of software design is,
    "How easy is it to make a plausible change?"

---

## A Generic Driver

-   Main function

[%inc invperc.py keep=main %]

---

## Setting Up

-   Relies on a setup function
    -  Can easily replace this in future with something that reads parameters from a file

[%inc invperc.py keep=setup %]

---

## Refactoring

-   We're going to build (at least) two grid classes, so import both here

[%inc invperc.py keep=import %]

-   Initialization relies on the grid's constructor
    -   All grids take the same parameters in the same order

[%inc invperc.py keep=initialize_grid %]

---

## Printing

-   Keep printing here
    -   Could have grids print themselves

[%inc invperc.py keep=print_grid %]

---

## Generic Grids

-   First grid is an [abstract](g:abc)e class" %]
    -   Defines common behaviors
    -   Declaring [abstract](g:abstract_method)hods" %]
        forces derived classes to provide a way to get and set item by location

[%inc grid_generic.py keep=main %]

---

## Other Methods

-   All other operations rely on these abstract methods
    -   Including the ones the derived classes have to implement
-   E.g. filling

[%inc grid_generic.py keep=fill %]

---

## Equality

-   Relying on interface allows us to implement equality test
    between grids with different underlying data representations

[%inc grid_generic.py keep=eq %]

---

## List-Based Grid

[%inc grid_list.py keep=gridlist %]

---

## Array-Based Grid

-   And another that uses a NumPy array

[%inc grid_array.py keep=gridarray %]

---

## And Now, Testing

-   `test_grid_start.py` tests that grids can be initialized
    -   But we don't know if we're getting the actual values from the grid because they're random
    -   And repeating the test for different classes is error-prone as well as annoying

[%inc test_grid_start.py keep=array_constructed_correctly %]
[%inc test_grid_start.py keep=list_constructed_correctly %]

---

## Injecting What We Need

-   Create a new class `GridListRandomizer` that takes a number generator as a constructor parameter
    -   Generate a grid filled with known values for testing

[%inc grid_list_randomizer.py keep=init %]

---

## Test Using Injection

-   Test looks better

[%inc test_grid_randomizer.py keep=list_with_randomizer_function %]

-   But we're no longer testing our actual grid class
    -   Could add extra arguments for all sorts of things to all our classes, but that's a lot of work

---

## Better Tools: Mock Objects

-   `test_grid_mock.py` replaces the random number generator with a [mock](g:mock_object)ect" %]
    without modifying the grid class

[%inc test_grid_mock.py keep=list_patching_randomization %]

---

## Better Tools: Parameterized Tests

-   `test_grid_parametrize.py` [parameterizes](g:parameterize_test) the test across both classes

[%inc test_grid_parametrize.py keep=list_parameterizing_classes %]

---

## A Testable Grid

-   `grid_filled.py` defines `GridFilled`, which we can populate with whatever data we want

[%inc grid_filled.py keep=init %]

---

## Using the Testable Grid

-   `test_grid_filled.py` starts by testing that filling from specified works correctly

[%inc test_grid_filled.py keep=explicit_filling_fills_correctly %]

-   Add test for filling grid by creating deterministic filling path

[%inc test_grid_filled.py keep=filling_with_straight_run_to_edge %]

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
