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

```{data-file="parse_01.py"}
import argparse
import csv
from datetime import date


HEADER = (
    ("id", int),
    ("specimen", str),
    ("date", date.fromisoformat),
    ("by", str),
    ("machine", str),
)


def cmdline_args():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--files", nargs="+", required=True, help="filenames")
    return parser.parse_args()


def parse_assay(filename):
    """Parse specified assay file."""

    with open(filename, "r") as reader:
        rows = [r for r in csv.reader(reader)]
    result = {}
    for i, (key, converter) in enumerate(HEADER):
        if rows[i][0] != key:
            raise ValueError(f"row {i} of {filename}: expected {key} got {rows[i][0]}")
        result[key] = converter(rows[i][1])
    return result


if __name__ == "__main__":
    args = cmdline_args()
    for filename in args.files:
        assay = parse_assay(filename)
        print(assay)
```

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

```{data-file="parse_02.py"}
import argparse
import csv
from datetime import date

import polars as pl


HEADER = (
    ("id", int),
    ("specimen", str),
    ("date", date.fromisoformat),
    ("by", str),
    ("machine", str),
)


def cmdline_args():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--files", nargs="+", required=True, help="filenames")
    return parser.parse_args()


def parse_assay(filename):
    """Parse specified assay file."""

    with open(filename, "r") as reader:
        rows = [r for r in csv.reader(reader)]
    result = _parse_header(rows)
    result["data"] = _parse_body(rows)
    return result


def _parse_body(rows):
    """Parse the body."""

    header_len = len(HEADER)
    schema = rows[header_len]
    schema[0] = "row"
    df = pl.DataFrame(rows[header_len + 1 :], orient="row", schema=schema)
    return df.with_columns(
        pl.col("row").cast(pl.Int64), pl.col("*").exclude("row").cast(pl.Float64)
    )


def _parse_header(rows):
    """Parse the header."""

    result = {}
    for i, (key, converter) in enumerate(HEADER):
        if rows[i][0] != key:
            raise ValueError(f"row {i} of {filename}: expected {key} got {rows[i][0]}")
        result[key] = converter(rows[i][1])
    return result


if __name__ == "__main__":
    args = cmdline_args()
    for filename in args.files:
        assay = parse_assay(filename)
        print(assay)
```

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

```{data-file="parse_03.py"}
import argparse
import csv
from datetime import date

import polars as pl


HEADER_LEN = 5


def cmdline_args():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--files", nargs="+", required=True, help="filenames")
    return parser.parse_args()


def parse_assay(filename, people):
    """Parse specified assay file."""

    with open(filename, "r") as reader:
        rows = [r for r in csv.reader(reader)]
    consumed, result = _parse_header(rows, people)
    result["data"] = _parse_body(rows)
    return result


def _convert_id(value, extra=None):
    """Convert assay ID that might be quoted."""

    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    return int(value)


def _convert_specimen(value, extra=None):
    """Convert specimen ID."""

    return value


def _convert_date(value, extra=None):
    """Convert ISO formatted date."""

    return date.fromisoformat(value)


def _convert_by(value, extra):
    """Convert person ID or name."""

    return value


def _convert_machine(value, extra=None):
    """Convert machine ID."""

    return value


def _parse_body(rows):
    """Parse the body."""

    schema = rows[HEADER_LEN]
    schema[0] = "row"
    df = pl.DataFrame(rows[HEADER_LEN + 1 :], orient="row", schema=schema)
    return df.with_columns(
        pl.col("row").cast(pl.Int64), pl.col("*").exclude("row").cast(pl.Float64)
    )


def _parse_header(rows, people):
    """Parse the header."""

    converters = (
        ("id", _convert_id),
        ("specimen", _convert_specimen),
        ("date", _convert_date),
        ("by", _convert_by),
        ("machine", _convert_machine),
    )
    assert len(converters) == HEADER_LEN, (
        "mis-match in converter table and header length"
    )

    result = {}
    i = 0
    for key, converter in converters:
        if rows[i][0] != key:
            result[key] = None
        else:
            result[key] = converter(rows[i][1], people)
            i += 1

    return i, result


if __name__ == "__main__":
    args = cmdline_args()
    people = {"Kristi Nõmmik": "nk3892"}
    for filename in args.files:
        assay = parse_assay(filename, people)
        print(assay)
```

## Machines

```{data-file="parse_04.py"}
import argparse
import csv
from datetime import date

import polars as pl


HEADER_LEN = 5


def cmdline_args():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--files", nargs="+", required=True, help="filenames")
    return parser.parse_args()


def parse_assay(filename, people):
    """Parse specified assay file."""

    with open(filename, "r") as reader:
        rows = [r for r in csv.reader(reader)]
    consumed, result = _parse_header(rows, people)
    result["data"] = _parse_body(filename, rows[consumed:])
    return result


def _convert_id(value, extra=None):
    """Convert assay ID that might be quoted."""

    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    return int(value)


def _convert_specimen(value, extra=None):
    """Convert specimen ID."""

    return value


def _convert_date(value, extra=None):
    """Convert ISO formatted date."""

    return date.fromisoformat(value)


def _convert_by(value, extra):
    """Convert person ID or name."""

    if value in extra:
        return extra[value]
    return value


def _convert_machine(value, extra=None):
    """Convert machine ID."""

    return value


def _parse_body(filename, rows):
    """Parse the body."""

    schema = rows[0]
    schema[0] = "row"
    df = pl.DataFrame(rows[1:], orient="row", schema=schema)
    return df.with_columns(
        pl.col("row").cast(pl.Int64), pl.col("*").exclude("row").cast(pl.Float64)
    )


def _parse_header(rows, people):
    """Parse the header."""

    converters = (
        ("id", _convert_id),
        ("specimen", _convert_specimen),
        ("date", _convert_date),
        ("by", _convert_by),
        ("machine", _convert_machine),
    )
    assert len(converters) == HEADER_LEN, (
        "mis-match in converter table and header length"
    )

    result = {}
    i = 0
    for key, converter in converters:
        if rows[i][0] != key:
            result[key] = None
        else:
            result[key] = converter(rows[i][1], people)
            i += 1

    return i, result


if __name__ == "__main__":
    args = cmdline_args()
    people = {"Kristi Nõmmik": "nk3892"}
    for filename in args.files:
        assay = parse_assay(filename, people)
        print(assay)
```

-   Loop over available header keys, incrementing count as we find a match
    -   Store `None` for missing values
    -   Probably cause headaches down the line
-   Modifiy `parse_header` to return the number of rows processed
    so that we can pass the right rows to `parse_body`

## Indented Body

```{data-file="parse_05.py"}
import argparse
import csv
from datetime import date

import polars as pl


HEADER_LEN = 5


def cmdline_args():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--files", nargs="+", required=True, help="filenames")
    return parser.parse_args()


def parse_assay(filename, people):
    """Parse specified assay file."""

    with open(filename, "r") as reader:
        rows = [r for r in csv.reader(reader)]
    consumed, result = _parse_header(rows, people)
    result["data"] = _parse_body(filename, rows[consumed:])
    return result


def _convert_id(value, extra=None):
    """Convert assay ID that might be quoted."""

    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    return int(value)


def _convert_specimen(value, extra=None):
    """Convert specimen ID."""

    return value


def _convert_date(value, extra=None):
    """Convert ISO formatted date."""

    return date.fromisoformat(value)


def _convert_by(value, extra):
    """Convert person ID or name."""

    if value in extra:
        return extra[value]
    return value


def _convert_machine(value, extra=None):
    """Convert machine ID."""

    return value


def _parse_body(filename, rows):
    """Parse the body."""

    if rows[0][1] == "":
        assert all(r[0] == "" for r in rows), f"Badly indented table in {filename}"
        rows = [r[1:] for r in rows]

    schema = rows[0]
    schema[0] = "row"
    df = pl.DataFrame(rows[1:], orient="row", schema=schema)
    return df.with_columns(
        pl.col("row").cast(pl.Int64), pl.col("*").exclude("row").cast(pl.Float64)
    )


def _parse_header(rows, people):
    """Parse the header."""

    converters = (
        ("id", _convert_id),
        ("specimen", _convert_specimen),
        ("date", _convert_date),
        ("by", _convert_by),
        ("machine", _convert_machine),
    )
    assert len(converters) == HEADER_LEN, (
        "mis-match in converter table and header length"
    )

    result = {}
    i = 0
    for key, converter in converters:
        if rows[i][0] != key:
            result[key] = None
        else:
            result[key] = converter(rows[i][1], people)
            i += 1

    return i, result


if __name__ == "__main__":
    args = cmdline_args()
    people = {"Kristi Nõmmik": "nk3892"}
    for filename in args.files:
        assay = parse_assay(filename, people)
        print(assay)
```

-   If the first row of the body starts with two blank columns:
    1.  Check that all the rest start with one blank column
    2.  [Dedent](g:dedent) the data
