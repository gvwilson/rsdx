---
title: "Initial Invasion Percolation Script"
tag: "A walk through the kind of code most scientists write."
syllabus:
- FIXME
---

- Initial version of invasion percolation.
  - At least it's broken into functions.
- Had to modify `print_grid` to show numeric values for debugging
  and to show settings (esp. `seed`) for reproducibility.
- Had to modify `main` to allow seed to be set from command line.
- No way to get the random seed back from `random`, so use a trick to make reproducible.
- Use `make demo` to run program.
