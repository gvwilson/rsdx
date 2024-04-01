-   [%b Bentley1982 %] changed how I see programming
    -   Speed doesn't always matter, but when it does, it really does
    -   There are widely-useful techniques for improving performance (e.g., spending memory to save time)
    -   *We can and should tackle this experimentally*
    -   If "software engineering" means anything, it ought to mean this

## Reproducibility {: #perf-repro}

-   Use `dataclasses` module to create a `Params` class in `params_single.py`
    -   Could use a dictionary or similar instead
    -   But this is a step toward something larger
-   Can now save parameters in version control.

[%inc params_single.py pattern=class:ParamsSingle %]

-   Modify code in `invperc_single.py` to use these parameters

[%inc invperc_single.py pattern=func:main %]

-   Load parameters from JSON file
    -   Could easily use YAML instead
    -   [%g spread "Spread" %] values into dataclass constructor

[%inc invperc_util.py pattern=func:get_params %]

-   Name the output file based on input parameters
    -   Would be nice if there was a standard way to embed parameters in the plot itself

## Performance {: #perf-perf}

-   Application's performance usually depends on what exactly it's doing
    -   So we [%g parameter_sweeping "sweep" %] the range of parameters to see how performance changes
-   Create another dataclass that stores multiple values for interesting parameters

[%inc params_sweep.py pattern=class:ParamsSweep %]

-   Then write a new `main` to try each combination of parameter values

[%inc invperc_sweep.py pattern=func:main %]

-   Could generate a list of parameter combinations
-   Instead, use a [%g generator "generator" %] to produce one at a time

[%inc invperc_sweep.py pattern=func:generate_sweep %]

-   Save results as CSV and plot

[% figure
   slug="perf_example"
   img="./k+list+array_z+35+55+75+95+115_d+2+10+100_r+50_s+556677.svg"
   caption="Running times for various depths and sizes."
   alt="Line graph showing that running time increases quadratically with grid size."
%]

-   NumPy array is *worse* than list-of-lists
    -   We're constantly [%g boxing "boxing" %] and [%g unboxing "unboxing" %] values
-   More important: runtime is growing faster than linear
    -   Which makes sense: we are searching N<sup>2</sup> cells each time we fill one

## Profiling {: #perf-profile}

-   A [%g profiler "profiler" %] records how much time is spent on each line of code
    -   Either by instrumenting it
    -   Or by sampling location periodically
-   Use Python's [`cProfile`][profile] module

[%inc run_profile.py mark="main" %]
[%inc profile_head.txt %]

-   We are spending most of our time in adjacency tests
-   Most of which are re-checking things we knew before
-   If we want to make this faster, this is what we need to fix

## Exercises {: #perf-exercises}

[%fixme "add exercises for performance profiling" %]
