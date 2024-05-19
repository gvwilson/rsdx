---
template: slides
title: "Cleanup"
tagline: "Refactor and test a script that models the spread of pollution."
abstract: >
    Computational notebooks are great for exploratory work,
    but research software engineers must also be able to create
    software libraries that can be re-mixed and re-used.
    This lesson therefore refactors a script
    that uses invasion percolation to simulate to model the spread of pollution
    and introduces several tools that can make testing research software easier,
    including the use of mock objects to make randomness less random
    and the use of coverage tools to determine
    what is and isn't being tested.
syllabus:
-   Break code into comprehensible chunks.
-   Create classes and class hierarchies.
-   Write docstrings and generating documentation pages.
-   Validate implementations against one another.
-   A quick review of pytest.
-   Deciding what tests to write.
-   Creating and using mock objects.
-   Making "random" reproducible.
-   Using coverage to determine what is and isn't being tested.
---

## The Problem

-   Refactor and test a program that (kind of) works to create something sturdier
-   Program models [%g inv_perc "invasion percolation" %]
    -   Grid of random numbers
    -   Fill the center cell
    -   Repeatedly:
        -   Find the cell adjacent to the filled region with the lowest value
	-   Fill it
    -   Until we reach the edge
-   Models spread of pollutant through fractured rock (among other things)

---

## Main Body of Original Script

-   Note: [%g rng_seed "random number seed" %] is optional

[%inc script.py mark=main %]

---

## The Grid

-   Make a grid as a list of lists
    -   Has a docstring

[%inc script.py pattern=func:make_grid %]

---

## Choosing the Next Cell

-   Sweep the whole grid

[%inc script.py pattern=func:choose_cell %]

---

## Helper Functions

-   Test adjacency

[%inc script.py pattern=func:adjacent %]

---

## Helper Functions

-   We also need to test if we're on the border

[%inc script.py pattern=func:on_border %]

---

## Display

-   And finally, show the result

[%inc script.py pattern=func:print_grid %]

---

## Critique

-   What if we want to change the way the grid is implemented?
-   Or the way we search for the next cell to fill?
-   Most meaningful measure of the quality of software design is,
    "How easy is it to make a plausible change?"

---

## A Generic Driver

-   Main function

[%inc invperc.py pattern=func:main %]

---

## Setting Up

-   Relies on a setup function
    -  Can easily replace this in future with something that reads parameters from a file

[%inc invperc.py pattern=func:setup %]

---

## Refactoring

-   We're going to build (at least) two grid classes, so import both here

[%inc invperc.py mark=import %]

-   Initialization relies on the grid's constructor
    -   All grids take the same parameters in the same order

[%inc invperc.py pattern=func:initialize_grid %]

---

## Printing

-   Keep printing here
    -   Could have grids print themselves

[%inc invperc.py pattern=func:print_grid %]

---

## Generic Grids

-   First grid is an [%g abc "abstract base class" %]
    -   Defines common behaviors
    -   Declaring [%g abstract_method "abstract methods" %]
        forces derived classes to provide a way to get and set item by location

[%inc grid_generic.py mark=main %]

---

## Other Methods

-   All other operations rely on these abstract methods
    -   Including the ones the derived classes have to implement
-   E.g. filling

[%inc grid_generic.py pattern="class:GridGeneric meth:fill" %]

---

## Equality

-   Relying on interface allows us to implement equality test
    between grids with different underlying data representations

[%inc grid_generic.py pattern="class:GridGeneric meth:__eq__" %]

---

## List-Based Grid

[%inc grid_list.py pattern="class:GridList" %]

---

## Array-Based Grid

-   And another that uses a NumPy array

[%inc grid_array.py pattern="class:GridArray" %]

---

## And Now, Testing

-   `test_grid_start.py` tests that grids can be initialized
    -   But we don't know if we're getting the actual values from the grid because they're random
    -   And repeating the test for different classes is error-prone as well as annoying

[%inc test_grid_start.py pattern=func:test_grid_array_constructed_correctly %]
[%inc test_grid_start.py pattern=func:test_grid_list_constructed_correctly %]

---

## Injecting What We Need

-   Create a new class `GridListRandomizer` that takes a number generator as a constructor parameter
    -   Generate a grid filled with known values for testing

[%inc grid_list_randomizer.py pattern="class:GridListRandomizer meth:__init__" %]

---

## Test Using Injection

-   Test looks better

[%inc test_grid_randomizer.py pattern="func:test_grid_list_with_randomizer_function" %]

-   But we're no longer testing our actual grid class
    -   Could add extra arguments for all sorts of things to all our classes, but that's a lot of work

---

## Better Tools: Mock Objects

-   `test_grid_mock.py` replaces the random number generator with a [%g mock_object "mock object" %]
    without modifying the grid class

[%inc test_grid_mock.py pattern="func:test_grid_list_patching_randomization" %]

---

## Better Tools: Parameterized Tests

-   `test_grid_parametrize.py` [%g parameterize_test "parameterizes" %] the test across both classes

[%inc test_grid_parametrize.py pattern="func:test_grid_list_parameterizing_classes" %]

---

## A Testable Grid

-   `grid_filled.py` defines `GridFilled`, which we can populate with whatever data we want

[%inc grid_filled.py pattern="class:GridFilled meth:__init__" %]

---

## Using the Testable Grid

-   `test_grid_filled.py` starts by testing that filling from specified works correctly

[%inc test_grid_filled.py pattern="func:test_explicit_filling_fills_correctly" %]

-   Add test for filling grid by creating deterministic filling path

[%inc test_grid_filled.py pattern="func:test_filling_with_straight_run_to_edge" %]

---

## Oops

-   But suddenly realize: what happens when several fillable cells have the same value?
    -   `fill_grid` always chooses the first one it encounters in this case
    -   So filling has a bias toward the (0,0) corner of the grid
-   [%x perf %] will tackle this problem
-   But first, let's see how fast our code is…

---

## Exercises

1.  Refactor grid classes so that we have a patchable method for filling initial values.
