---
template: slides
title: "Performance"
tagline: "Compare grid implementations empirically."
abstract: >
    Some pieces of research software have to be fast in order to be useful.
    This lesson therefore explores
    how to capture program parameters in reproducible ways,
    how profiling can help us figure out which parts of our program are worth optimizing,
    and how being lazy can make programs faster.
syllabus:
-   Introduce Python type annotations.
-   Define dataclasses to represent parameters for profiling runs.
-   Using cProfile to determine which parts are expensive.
-   Tuning code does not solve algorithmic problems like quadratic growth in runtime.
-   Estimating algorithm performance with big-oh.
-   Extending a class hierarchy to accommodate new features.
-   Adapting tools written earlier to make all of this simpler to run, test, and document.
---

## The Problem

-   Speed doesn't always matter, but when it does, it really does
-   There are widely-useful techniques for improving performance (e.g., spending memory to save time)
-   *We can and should tackle this experimentally*
    -   If "software engineering" means anything, it ought to mean this

---

## Reproducibility

-   Use `dataclasses` module to create a `Params` class in `params_single.py`
    -   Could use a dictionary or similar instead
    -   But this is a step toward something larger
-   Can now save parameters in version control

[%inc params_single.py pattern=class:ParamsSingle %]

---

## Saving Prameters

-   Load parameters from JSON file
    -   Could easily use YAML instead
    -   [%g spread "Spread" %] values into dataclass constructor

[%inc invperc_util.py pattern=func:get_params %]

---

## Using Parameters

-   Modify code in `invperc_single.py` to use these parameters

[%inc invperc_single.py pattern=func:main %]

-   Would be nice if there was a standard way to embed parameters in the plot itself

---

## Performance

-   Application's performance usually depends on what exactly it's doing
    -   So we [%g parameter_sweeping "sweep" %] the range of parameters to see how performance changes
-   Create another dataclass to store multiple values for interesting parameters

[%inc params_sweep.py pattern=class:ParamsSweep %]

---

## Sweeping Parameter Ranges

-   Next, rewrite `main` to try each combination of parameter values

[%inc invperc_sweep.py pattern=func:main %]

---

## Generators

-   Could generate a list of parameter combinations
-   Instead, use a [%g generator "generator" %] to produce one at a time

[%inc invperc_sweep.py pattern=func:generate_sweep %]

---

## Results

-   Save results as CSV and plot

[% figure
   slug="perf_example"
   img="./k+list+array_z+35+55+75+95+115_d+2+10+100_r+50_s+556677.svg"
   caption="Running times for various depths and sizes."
   alt="Line graph showing that running time increases quadratically with grid size."
%]

---

## That's a Surprise

-   NumPy array is *worse* than list-of-lists
    -   We're constantly [%g boxing "boxing" %] and [%g unboxing "unboxing" %] values
-   More important: runtime is growing faster than linear
    -   Which makes sense: we are searching \\( N^2 \\) cells each time we fill one

---

## Profiling

-   A [%g profiler "profiler" %] records how much time is spent on each line of code
    -   Either by instrumenting it
    -   Or by sampling location periodically
-   Use Python's [`cProfile`][profile] module

[%inc run_profile_list.py mark="main" %]

---

## Where the Time Goes

[%inc profile_list_head.txt %]

-   We are spending most of our time in adjacency tests
    -   Most of which are re-checking things we knew before
-   If we want to make our program faster, this is what we need to fix

---

## Better is Possible

-   Start with the punchline and work backward

[% figure
   slug="perf_lazy"
   img="./k+lazy+list+array_z+35+55+75+95+115_d+2+10+100_r+50_s+556677.svg"
   caption="Running times for various depths and sizes."
   alt="Line graph showing that the lazy algorithm's performance is nearly flat."
%]

---

## Lazy Evaluation

-   We have been searching the entire grid to find the next cell to fill
    -   But we only need to look on the border
    -   And we can keep track of where the border is
-   Keep a dictionary called `candidates`
    -   Key: a value in the grid
    -   Values: coordinates of cells on the border that have that value
-   On each step:
    -   Find the lowest key
    -   Choose and fill one of its cells at random (to solve the bias problem of [%x cleanup %])
    -   Add its unfilled neighbors to `candidates`
-   Trading space for time
    -   Storing cell values and coordinates is redundant
    -   But filling a cell now takes constant time regardless of grid size

---

## A Lazy Grid

-   `GridLazy` constructor

[%inc grid_lazy.py pattern="class:GridLazy meth:__init__" %]

---

## Lazy Filling

-   Filling algorithm overrides inherited method
    -   Fill the center cell
    -   Add its neighbors as candidates
    -   Repeatedly choose a cell to fill (stopping if we've reached the boundary)

[%inc grid_lazy.py pattern="class:GridLazy meth:fill" %]

---

## Adding Candidates

[%inc grid_lazy.py pattern="class:GridLazy meth:add_candidates" %]
[%inc grid_lazy.py pattern="class:GridLazy meth:add_one_candidate" %]

---

## Choosing a Cell

[%inc grid_lazy.py pattern="class:GridLazy meth:choose_cell" %]

---

## It's Faster

-   Sweep the same parameter ranges as before
-   Performance is much better
    -   Searching an \\( N{\times}N \\) grid is \\( N^2 \\) operations
    -   Fill about \\( N^{1.5} \\) cells (it's a fractal)
    -   So running time of the naïve approach is proportional to \\( N^{3.5} \\)
    -   Which a computer scientist would write \\( \mathcal{O}(N^{3.5}) \\)
    -   Running time of lazy approach is just \\( \mathcal{O}(N^{1.5}) \\)
-   So it is *fundamentally* faster

---

## Exercises {: #lazy-exercises}

1.  [%fixme "add exercises for performance profiling" %]

1.  Modify the list and array implementation to collect candidate cells of equal lowest value
    and select one of those.

1.  Does it make sense to pre-populate `candidates` by adding *all* cells in the grid
    at the start of the program?
    Why or why not?

1.  [%fixme "test lazy approach with randomnmess" %]
