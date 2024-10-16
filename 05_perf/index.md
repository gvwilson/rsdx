# Performance

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

[%inc params_single.py keep=paramssingle %]

---

## Saving Prameters

-   Load parameters from JSON file
    -   Could easily use YAML instead
    -   [Spread](g:spread) values into dataclass constructor

[%inc invperc_util.py keep=get_params %]

---

## Using Parameters

-   Modify code in `invperc_single.py` to use these parameters

[%inc invperc_single.py keep=main %]

-   Would be nice if there was a standard way to embed parameters in the plot itself

---

## Performance

-   Application's performance usually depends on what exactly it's doing
    -   So we [sweep](g:parameter_sweeping) the range of parameters to see how performance changes
-   Create another dataclass to store multiple values for interesting parameters

[%inc params_sweep.py keep=paramssweep %]

---

## Sweeping Parameter Ranges

-   Next, rewrite `main` to try each combination of parameter values

[%inc invperc_sweep.py keep=main %]

---

## Generators

-   Could generate a list of parameter combinations
-   Instead, use a [generator](g:generator) to produce one at a time

[%inc invperc_sweep.py keep=generate_sweep %]

---

## Results

-   Save results as CSV and plot

[% figure
   id="perf_example"
   src="./k+list+array_z+35+55+75+95+115_d+2+10+100_r+50_s+556677.svg"
   caption="Running times for various depths and sizes."
   alt="Line graph showing that running time increases quadratically with grid size."
%]

---

## That's a Surprise

-   NumPy array is *worse* than list-of-lists
    -   We're constantly [boxing](g:boxing) and [unboxing](g:unboxing) values
-   More important: runtime is growing faster than linear
    -   Which makes sense: we are searching \\( N^2 \\) cells each time we fill one

---

## Profiling

-   A [profiler](g:profiler) records how much time is spent on each line of code
    -   Either by instrumenting it
    -   Or by sampling location periodically
-   Use Python's [`cProfile`][profile] module

[%inc run_profile_list.py keep=main %]

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
   id="perf_lazy"
   src="./k+lazy+list+array_z+35+55+75+95+115_d+2+10+100_r+50_s+556677.svg"
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
    -   Choose and fill of its cells at random to eliminate the bias of [the previous chapter](../04_cleanup/index.md)
    -   Add its unfilled neighbors to `candidates`
-   Trading space for time
    -   Storing cell values and coordinates is redundant
    -   But filling a cell now takes constant time regardless of grid size

---

## A Lazy Grid

-   `GridLazy` constructor

[%inc grid_lazy.py keep=init %]

---

## Lazy Filling

-   Filling algorithm overrides inherited method
    -   Fill the center cell
    -   Add its neighbors as candidates
    -   Repeatedly choose a cell to fill (stopping if we've reached the boundary)

[%inc grid_lazy.py keep=fill %]

---

## Adding Candidates

[%inc grid_lazy.py keep=add_candidates %]
[%inc grid_lazy.py keep=add_one_candidate %]

---

## Choosing a Cell

[%inc grid_lazy.py keep=choose_cell %]

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

1.  FIXME: add exercises for performance profiling

1.  Modify the list and array implementation to collect candidate cells of equal lowest value
    and select one of those.

1.  Does it make sense to pre-populate `candidates` by adding *all* cells in the grid
    at the start of the program?
    Why or why not?

1.  FIXME: test lazy approach with randomnmess
