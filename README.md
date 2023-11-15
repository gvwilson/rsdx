# Research Software Design by Example

Examples of software design in research software engineering.

1.  Convert some messy CSV data files with geocoded pollution measurements into tidy CSV.

1.  Use the tidy data to try to find the center point of each polluted region and visualize it.

1.  Walk the reader through a student-quality Python script that uses invasion percolation to model pollution spread.

1.  Refactor that script into classes with two different grid implementations.

1.  Measure the performance of those two implementations in order to pick one.

1.  Convert the measurement scripts to use a pipeline runner.

1.  Introduce the idea of big-oh and use it to explain why a lazy implementation of percolation is so much faster.

1.  Use box-counting to estimate the fractal dimension and compare to density vs. distance.
    -   Use this to motivate use of DVC to manage files that are too large for Git.

1.  Show how to use mocks to test a program like invasion percolation that relies on pseudo-randomness.

1.  Analyze genomic data from snails to see if a single mutation accounts for differences in sizes.
    - Building toward modeling pollutant impact on snails.

1.  Use a random walk to estimate lifetime dosage for snails in polluted areas and figure out why the results are odd.
