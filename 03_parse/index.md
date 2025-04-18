# Parsing Messy Data

## The Problem

-   Our analysis pipeline is going to process data from microplates
    -   Rectangular arrangements of tiny wells in inert plastic
    -   Each well contains a sample or a control
    -   Treat with chemicals, wait, photograph, and measure brightness of each well
-   All of our lab machines are supposed to generate files with the same format
-   But some don't match the spec

## Expected

-   [`003805_readings.csv`](003805_readings.csv)

| Row | Field      | Purpose      | Type    | Example    |
| --: | ---------- | ------------ | ------- | ---------- |
|   1 | `id`       | assay ID     | integer | 003805     |
|   2 | `specimen` | specimen ID  | text    | VPVCOP     |
|   3 | `date`     | assay date   | date    | 2024-03-13 |
|   4 | `by`       | scientist ID | text    | nk3892     |
|   5 | `machine`  | machine ID   | text    | M0004      |

-   And then a table of readings with alphabetically labeled columns
    and numerically labeled rows
-   Hm: are the leading 0's in the assay ID significant?

|    | A    | B    | C    | D    |
| -: | ---: | ---: | ---: | ---: |
|  1 | 0.03 | 0.27 | 0.11 | 0.94 |
|  2 | 0.61 | 1.00 | 0.66 | 0.04 |
|  3 | 0.78 | 0.58 | 0.06 | 0.74 |
|  4 | 0.01 | 0.18 | 0.74 | 0.01 |

## Problems We've Seen

-   `id` is wrapped in quotes to make it a string instead of a number
-   Table of readings is indented one column
-   `by` is a name rather than a person ID

## Strategy

-   Easy then hard
    -   Write a parser for the good case
    -   Then modify it for the other cases
    -   And then write tests
-   Result?
    -   For now, a dictionary with keys for the header values
        and a [Polars][polars] dataframe for the body

## Header First

[`parse_01.py`](./parse_01.py)

-   `HEADER` is a table of expected keys and conversion functions
    -   Functions are just another kind of data
-   Read all the rows with a list comprehension
-   Loop over the header and check the keys
-   Convert the values

## The Table

-   Options
    1.  Re-read the file with Polars, telling it to skip header rows
    2.  Make the dataframe from the rows we have in memory
-   The second option might be more efficient, but that's *not* a good reason to choose it
    -   The difference will be miniscule for small data like ours
    -   And we know we're going to have to handle malformed data

## The Table (cont.)

[`parse_02.py`](./parse_02.py)

-   Refactor parser to call one [helper function](g:helper_function) for the head
    and another for the body
    -   Name these with a leading underscore to signal that they're for internal use
-   Create a [schema](g:schema) to tell Polars what to call the columns
-   And the [cast](g:cast) the strings to integers and floating-point numbers

## Handling Problems

-   We need a lookup table of person names to person IDs
    -   Worry later about where we'll get the data
-   Which means we need to pass an extra argument to the conversion functions
-   So write our own wrappers
-   And move the table into `_parse_header` because the functions need to be defined
    -   Add an `assert` to check our coding
-   Test it out by stripping quotes from assay IDs and looking up names

[`parse_03.py`](./parse_03.py)

## Machines

[`parse_04.py`](./parse_04.py)

-   Loop over available header keys, incrementing count as we find a match
    -   Store `None` for missing values
    -   Probably cause headaches down the line
-   Modifiy `parse_header` to return the number of rows processed
    so that we can pass the right rows to `parse_body`

## Indented Body

[`parse_05.py`](./parse_05.py)

-   If the first row of the body starts with two blank columns:
    1.  Check that all the rest start with one blank column
    2.  [Dedent](g:dedent) the data
