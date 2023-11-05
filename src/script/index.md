- Is broken into functions (yay).
- Had to modify `print_grid` to show numeric values for debugging
  and to show settings (esp. `seed`) for reproducibility.
- Had to modify `main` to allow seed to be set from command line.
- No way to get the random seed back from `random`, so use a trick to make reproducible.
