---
title: "Unit Tests"
tagline: "Use mocks to test programs that rely on pseudo-randomness."
syllabus:
-   A quick review of pytest.
-   Deciding what tests to write.
-   Creating and using mock objects.
-   Making "random" reproducible.
-   Using coverage to determine what is and isn't being tested.
---

## False Starts {: #test-start}

-   Use `GridList` and `GridArray` from [%x refactor %]
-   `test_grid_start.py` tests that grids can be initialized
    -   But we don't know if we're getting the actual values from the grid because they're random
    -   And repeating the test for different classes is error-prone as well as annoying

[%inc test_grid_start.py pattern=func:test_grid_array_constructed_correctly %]
[%inc test_grid_start.py pattern=func:test_grid_list_constructed_correctly %]

-   Create a new class `GridListRandomizer` that takes a number generator as a constructor parameter
    -   Generate a grid filled with known values for testing

[%inc grid_list_randomizer.py pattern="class:GridListRandomizer meth:__init__" %]

-   Test looks better

[%inc test_grid_randomizer.py pattern="func:test_grid_list_with_randomizer_function" %]

-   But we're no longer testing our actual grid class
    -   Could add extra arguments for all sorts of things to all our classes, but that's a lot of work

## Better Tools {: #test-tools}

-   `test_grid_mock.py` replaces the random number generator with a [%g mock_object "mock object" %]
    without modifying the grid class

[%inc test_grid_mock.py pattern="func:test_grid_list_patching_randomization" %]

-   `test_grid_parametrize.py` [%g parameterize_test "parameterizes" %] the test across both classes

[%inc test_grid_parametrize.py pattern="func:test_grid_list_parameterizing_classes" %]

## A Testable Grid {: #test-grid}

-   `grid_filled.py` defines `GridFilled`, which we can populate with whatever data we want

[%inc grid_filled.py pattern="class:GridFilled meth:__init__" %]

-   `test_grid_filled.py` starts by testing that filling from specified works correctly

[%inc test_grid_filled.py pattern="func:test_explicit_filling_fills_correctly" %]

-   Add test for filling grid by creating deterministic filling path

[%inc test_grid_filled.py pattern="func:test_filling_with_straight_run_to_edge" %]

-   But suddenly realize: what happens when several fillable cells have the same value?
    -   `fill_grid` always chooses the first one it encounters in this case
    -   So filling has a bias toward the (0,0) corner of the grid

## Exercises {: #test-exercises}

1.  Refactor grid classes so that we have a patchable method for filling initial values.
