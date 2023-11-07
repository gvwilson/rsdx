# Documentation

## src/parse

### `src/parse/parse.py`: Parse messy data files.

-   class `State`: Enumerate possible parser states.
-   function `main`: Main driver.
-   function `is_empty`: Is this row effectively empty?
-   function `is_start_of_body`: Is this row the start of the body section?
-   function `load`: Load messy data.
-   function `normalize`: Remove leading spaces from rows if necessary.
-   function `parse_args`: Parse command-line arguments.
-   function `split`: Split header from body.

## src/center

### `src/center/display.py`: Analyze pollution readings.

-   function `main`: Main driver.
-   function `read_csv`: Read CSV files directly into dataframes.
-   function `read_db_pandas`: Read database tables into Pandas dataframes and manipulate.
-   function `read_db_sql`: Read tables and do calculations directly in SQL.
-   function `combine_with_pandas`: Combine tables using Pandas.
-   function `check`: Check all tables against each other.
-   function `make_figures`: Create figures showing calculated results.
-   function `parse_args`: Parse command-line arguments.

## src/script

### `src/script/invperc.py`: Invasion percolation in Python.

-   function `main`: Main driver.
-   function `make_grid`: Create a width X height grid.
-   function `choose_cell`: Choose the next cell to fill in.
-   function `adjacent`: Is (x, y) adjacent to a filled cell?
-   function `on_border`: Is this cell on the border of the grid?
-   function `print_grid`: Show the result.

## src/grid

### `src/grid/invperc.py`: Invasion percolation in Python.

-   function `main`: Main driver.
-   function `setup`: Get parameters.
-   function `initialize_grid`: Prepare grid for simulation.
-   function `fill_grid`: Fill grid one cell at a time.
-   function `choose_cell`: Choose the next cell to fill.
-   function `print_grid`: Show the result.

### `src/grid/grid_list.py`: List-of-lists grid.

-   class `GridList`: Represent grid as list of lists.
    -   method `__init__`: Construct and fill.
    -   method `__getitem__`: Get value at location.
    -   method `__setitem__`: Set value at location.

### `src/grid/grid_array.py`: NumPy array grid.

-   class `GridArray`: Represent grid as NumPy array.
    -   method `__init__`: Construct and fill.
    -   method `__getitem__`: Get value at location.
    -   method `__setitem__`: Set value at location.

### `src/grid/grid_generic.py`: Represent 2D grid.

-   class `GridGeneric`: Represent a generic grid.
    -   method `__getitem__`: Get value at location.
    -   method `__setitem__`: Set value at location.
    -   method `__init__`: Record shared state.
    -   method `width`: Get width of grid.
    -   method `height`: Get height of grid.
    -   method `depth`: Get depth of grid.
    -   method `adjacent`: Is (x, y) adjacent to a filled cell?
    -   method `on_border`: Is this cell on the border of the grid?

## src/perf

### `src/perf/invperc.py`: Invasion percolation in Python.

-   function `main`: Main driver.
-   function `setup`: Get parameters.
-   function `run_all`: Run all variations.
-   function `initialize_grid`: Prepare grid for simulation.
-   function `fill_grid`: Fill grid one cell at a time.
-   function `choose_cell`: Choose the next cell to fill.
-   function `check_equal`: Check that all grids got the same answer.
-   function `print_grid`: Show the result.

### `src/perf/grid_list.py`: List-of-lists grid.

-   class `GridList`: Represent grid as list of lists.
    -   method `__init__`: Construct and fill.
    -   method `__getitem__`: Get value at location.
    -   method `__setitem__`: Set value at location.

### `src/perf/grid_array.py`: NumPy array grid.

-   class `GridArray`: Represent grid as NumPy array.
    -   method `__init__`: Construct and fill.
    -   method `__getitem__`: Get value at location.
    -   method `__setitem__`: Set value at location.

### `src/perf/grid_generic.py`: Represent 2D grid.

-   class `GridGeneric`: Represent a generic grid.
    -   method `__getitem__`: Get value at location.
    -   method `__setitem__`: Set value at location.
    -   method `__init__`: Record shared state.
    -   method `width`: Get width of grid.
    -   method `height`: Get height of grid.
    -   method `depth`: Get depth of grid.
    -   method `__eq__`: Compare to another grid.
    -   method `adjacent`: Is (x, y) adjacent to a filled cell?
    -   method `on_border`: Is this cell on the border of the grid?

## src/flow

### `src/flow/analysis.py`: Analyze data from runs.

-   function `main`: Main driver.
-   function `parse_args`: Parse command-line arguments.

### `src/flow/invperc.py`: Invasion percolation in Python.

-   function `main`: Main driver.
-   function `parse_args`: Get parameters.
-   function `initialize_random`: Initialize RNG in reproducible way.
-   function `percolate`: Run all simulations.
-   function `initialize_grid`: Prepare grid for simulation.
-   function `fill_grid`: Fill grid one cell at a time.
-   function `choose_cell`: Choose the next cell to fill.
-   function `check_equal`: Check that all grids got the same answer.
-   function `print_grid`: Show the result.

### `src/flow/flow.py`: Re-run everything.

-   class `InvPercFlow`: Metaflow for invasion percolation.
    -   method `start`: Collect parameters and run jobs.
    -   method `run_job`: Run a sweep with one set of parameters.
    -   method `join`: Combine results from all sweeps.
    -   method `end`: Save results.

### `src/flow/grid_list.py`: List-of-lists grid.

-   class `GridList`: Represent grid as list of lists.
    -   method `__init__`: Construct and fill.
    -   method `__getitem__`: Get value at location.
    -   method `__setitem__`: Set value at location.

### `src/flow/grid_array.py`: NumPy array grid.

-   class `GridArray`: Represent grid as NumPy array.
    -   method `__init__`: Construct and fill.
    -   method `__getitem__`: Get value at location.
    -   method `__setitem__`: Set value at location.

### `src/flow/grid_generic.py`: Represent 2D grid.

-   class `GridGeneric`: Represent a generic grid.
    -   method `__getitem__`: Get value at location.
    -   method `__setitem__`: Set value at location.
    -   method `__init__`: Record shared state.
    -   method `width`: Get width of grid.
    -   method `height`: Get height of grid.
    -   method `depth`: Get depth of grid.
    -   method `__eq__`: Compare to another grid.
    -   method `adjacent`: Is (x, y) adjacent to a filled cell?
    -   method `on_border`: Is this cell on the border of the grid?

## src/lazy

### `src/lazy/analysis.py`: Analyze data from runs.

-   function `main`: Main driver.
-   function `parse_args`: Parse command-line arguments.

### `src/lazy/invperc.py`: Invasion percolation in Python.

-   function `main`: Main driver.
-   function `setup`: Get parameters.
-   function `initialize_random`: Initialize RNG in reproducible way.
-   function `percolate`: Run all simulations.
-   function `initialize_grid`: Prepare grid for simulation.
-   function `fill_grid`: Fill grid one cell at a time.
-   function `check_equal`: Check that all grids got the same answer.
-   function `print_grid`: Show the result.

### `src/lazy/flow.py`: Re-run everything.

-   class `InvPercFlow`: Metaflow for invasion percolation.
    -   method `start`: Collect parameters and run jobs.
    -   method `run_job`: Run a sweep with one set of parameters.
    -   method `join`: Combine results from all sweeps.
    -   method `end`: Save results.

### `src/lazy/grid_lazy.py`: Lazy-filling grid.

-   class `GridLazy`: Only look at cells that might actually be filled next time.
    -   method `__init__`: Construct and fill.
    -   method `fill_first_cell`: Fill the initial cell.
    -   method `choose_cell`: Choose the next cell to fill.
    -   method `add_candidates`: Add candidates around (x, y).
    -   method `_add_candidate`: Add (x, y) if suitable.

### `src/lazy/grid_list.py`: List-of-lists grid.

-   class `GridList`: Represent grid as list of lists.
    -   method `__init__`: Construct and fill.
    -   method `__getitem__`: Get value at location.
    -   method `__setitem__`: Set value at location.

### `src/lazy/grid_array.py`: NumPy array grid.

-   class `GridArray`: Represent grid as NumPy array.
    -   method `__init__`: Construct and fill.
    -   method `__getitem__`: Get value at location.
    -   method `__setitem__`: Set value at location.

### `src/lazy/grid_generic.py`: Represent 2D grid.

-   class `GridGeneric`: Represent a generic grid.
    -   method `__getitem__`: Get value at location.
    -   method `__setitem__`: Set value at location.
    -   method `__init__`: Record shared state.
    -   method `width`: Get width of grid.
    -   method `height`: Get height of grid.
    -   method `depth`: Get depth of grid.
    -   method `__eq__`: Compare to another grid.
    -   method `adjacent`: Is (x, y) adjacent to a filled cell?
    -   method `on_border`: Is this cell on the border of the grid?
    -   method `fill_first_cell`: Fill the initial cell.
    -   method `choose_cell`: Choose the next cell to fill.

## src/dim

### `src/dim/grid.py`: Represent 2D grid.

-   class `Grid`: Represent a grid.
    -   method `__init__`: Construct and fill.
    -   method `width`: Get width of grid.
    -   method `height`: Get height of grid.
    -   method `depth`: Get depth of grid.
    -   method `__getitem__`: Get value at location.
    -   method `__setitem__`: Set value at location.
    -   method `__eq__`: Compare to another grid.
    -   method `fill`: Fill grid one cell at a time.
    -   method `adjacent`: Is (x, y) adjacent to a filled cell?
    -   method `on_border`: Is this cell on the border of the grid?
    -   method `fill_first_cell`: Fill the initial cell.
    -   method `choose_cell`: Choose the next cell to fill.
    -   method `add_candidates`: Add candidates around (x, y).
    -   method `print`: Show the result.
    -   method `_add_candidate`: Add (x, y) if suitable.
    -   method `_init_grid`: Initialize grid contents.

### `src/dim/invperc.py`: Invasion percolation in Python.

-   function `main`: Main driver.
-   function `setup`: Get parameters.
-   function `initialize_random`: Initialize RNG in reproducible way.
-   function `percolate`: Run all simulations.
-   function `measure_dimension`: Measure fractal dimension of grid.

### `src/dim/flow.py`: Re-run everything.

-   class `InvPercFlow`: Metaflow for invasion percolation.
    -   method `start`: Collect parameters and run jobs.
    -   method `run_job`: Run a sweep with one set of parameters.
    -   method `join`: Combine results from all sweeps.
    -   method `end`: Save results.

## src/density

### `src/density/grid.py`: Represent 2D grid.

-   class `Grid`: Represent a grid.
    -   method `__init__`: Construct and fill.
    -   method `width`: Get width of grid.
    -   method `height`: Get height of grid.
    -   method `depth`: Get depth of grid.
    -   method `__getitem__`: Get value at location.
    -   method `__setitem__`: Set value at location.
    -   method `__eq__`: Compare to another grid.
    -   method `fill`: Fill grid one cell at a time.
    -   method `adjacent`: Is (x, y) adjacent to a filled cell?
    -   method `on_border`: Is this cell on the border of the grid?
    -   method `fill_first_cell`: Fill the initial cell.
    -   method `choose_cell`: Choose the next cell to fill.
    -   method `add_candidates`: Add candidates around (x, y).
    -   method `print`: Show the result.
    -   method `_add_candidate`: Add (x, y) if suitable.
    -   method `_init_grid`: Initialize grid contents.

### `src/density/analysis.py`: Analyze data from runs.

-   function `main`: Main driver.
-   function `parse_args`: Parse command-line arguments.

### `src/density/invperc.py`: Invasion percolation in Python.

-   function `main`: Main driver.
-   function `setup`: Get parameters.
-   function `initialize_random`: Initialize RNG in reproducible way.
-   function `percolate`: Run all simulations.
-   function `calculate_density`: Calculate density versus distance from center of grid.

### `src/density/flow.py`: Re-run everything.

-   class `InvPercFlow`: Metaflow for invasion percolation.
    -   method `start`: Collect parameters and run jobs.
    -   method `run_job`: Run a sweep with one set of parameters.
    -   method `join`: Combine results from all sweeps.
    -   method `end`: Save results.

## src/test

### `src/test/grid.py`: Represent 2D grid.

-   class `Grid`: Represent a grid.
    -   method `__init__`: Construct and fill.
    -   method `width`: Get width of grid.
    -   method `height`: Get height of grid.
    -   method `depth`: Get depth of grid.
    -   method `__getitem__`: Get value at location.
    -   method `__setitem__`: Set value at location.
    -   method `__eq__`: Compare to another grid.
    -   method `sweep`: Return indices and values in order.
    -   method `on_border`: Is this cell on the border of the grid?
    -   method `print`: Show the result.
    -   method `overwrite`: Overwrite with values.

### `src/test/invperc.py`: Invasion percolation in Python.

-   function `main`: Main driver.
-   function `setup`: Get parameters.
-   function `initialize_random`: Initialize RNG in reproducible way.
-   function `percolate`: Run all simulations.
-   function `calculate_density`: Calculate density versus distance from center of grid.

### `src/test/filler.py`: Manage filling.

-   class `Filler`: Manage grid filling.
    -   method `__init__`: Construct.
    -   method `grid`: Get the grid object.
    -   method `fill`: Fill grid one cell at a time.
    -   method `fill_first_cell`: Fill the initial cell.
    -   method `choose_cell`: Choose the next cell to fill.
    -   method `add_candidates`: Add candidates around (x, y).
    -   method `_add_candidate`: Add (x, y) if suitable.
    -   method `_randomize`: Randomize grid contents.

