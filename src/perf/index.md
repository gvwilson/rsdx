-   Use `dataclasses` to create a `Params` class in `params_first.py`.
-   Modify code in `invperc_first.py` to use these parameters.
-   Can now save parameters in version control.
-   Name output file based on input parameters.

[% figure
   slug="perf_example"
   img="./k+list+array_z+35+55+75+95+115_d+2+10+100_r+50_s+556677.svg"
   caption="Running times for various depths and sizes."
   alt="Line graph showing that running time increases quadratically with grid size."
%]

-   Profiling with [`cProfile`][profile] shows that we're spending most of our time in adjacency tests.
-   Overall time is growing quadratically with grid size.
