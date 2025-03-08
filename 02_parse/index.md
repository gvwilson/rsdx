# Parsing Raw Data

## The Problem

-   We are studying the impact of toxic waste on snails on Vancouver Island
-   First step is to read data files with snail weight readings from four sample sites
-   But the files are formatted inconsistently

---

## The Data

-   First file looks like this

```{data-file="GBY.csv"}
Site:,GBY
site,date,lon,lat,reading
GBY,2023-05-08,-124.45981,48.92163,26.7
GBY,2023-05-08,-124.45932,48.92091,70.9
GBY,2023-05-08,-124.46036,48.92098,38.1
GBY,2023-05-08,-124.45743,48.92101,1.7
GBY,2023-05-08,-124.46048,48.92059,33.0
GBY,2023-05-08,-124.46061,48.92166,7.9
GBY,2023-05-08,-124.46004,48.92069,50.1
GBY,2023-05-08,-124.45828,48.92066,32.6
```

-   First row has only two columns (one of which includes the site ID, which we can check against the file name)
-   After that we have five nicely-formatted columns

---

## Just Read It

-   That seems simple

```{data-file="naive.py"}
import pandas as pd
import sys

df = pd.read_csv(sys.argv[1], skiprows=1)
print(df)
```
```{data-file="naive_GBY.out"}
  site        date        lon       lat  reading
0  GBY  2023-05-08 -124.45981  48.92163     26.7
1  GBY  2023-05-08 -124.45932  48.92091     70.9
2  GBY  2023-05-08 -124.46036  48.92098     38.1
3  GBY  2023-05-08 -124.45743  48.92101      1.7
4  GBY  2023-05-08 -124.46048  48.92059     33.0
5  GBY  2023-05-08 -124.46061  48.92166      7.9
6  GBY  2023-05-08 -124.46004  48.92069     50.1
7  GBY  2023-05-08 -124.45828  48.92066     32.6
```

---

## But…

-   Try it on the next file

```{data-file="naive_YOU.out"}
    Unnamed: 0 site        date        lon       lat  reading
0          NaN  YOU  2023-05-01 -124.19699  48.87250     96.6
1          NaN  YOU  2023-05-01 -124.19707  48.87281     70.0
2          NaN  YOU  2023-05-01 -124.19808  48.87288     41.7
3          NaN  YOU  2023-05-01 -124.19678  48.87271     87.6
4          NaN  YOU  2023-05-01 -124.19725  48.87254     83.8
5          NaN  YOU  2023-05-01 -124.19829  48.87155      5.4
6          NaN  YOU  2023-05-01 -124.19696  48.87250     72.8
7          NaN  YOU  2023-05-01 -124.19737  48.87231     74.9
8          NaN  YOU  2023-05-01 -124.19669  48.87268     43.0
9          NaN  YOU  2023-05-01 -124.19704  48.87257     94.2
10         NaN  YOU  2023-05-01 -124.19734  48.87358     15.9
11         NaN  YOU  2023-05-01 -124.19670  48.87378      4.5
```

-   Problem is that the readings are indented by one column

---

## And…

-   Next file has a blank line between header and readings

```{data-file="COW.csv"}
Site:,COW
Analyst:,P. Srinath

SITE,DATE,LON,LAT,READING
COW,2023-04-27,-124.04518,48.82171,106.9
COW,2023-04-27,-124.045,48.8216,81.7
```

-   And another one has *two* blank lines between the header and the data

---

## Options

1.  Edit the raw data files
    -   Never do this
2.  Copy and edit the files
    -   But it turns out each field scientist submitted dozens of files
    -   Each person was consistent, but editing them all by hand will be tedious and error-prone
3.  Write a parser
    -   Never do this…
    -   …unless you have to

---

## Overall Structure

-   Main body follows 50-year-old conventions for Unix command-line tools
    -   Get command-line arguments
    -   Read from standard input or a file (processing as we read)
    -   Write to standard output or a file

```{data-file="parse.py:main"}
def main():
    """Main driver."""
    args = parse_args()

    if args.infile:
        with open(args.infile, "r") as reader:
            df = load(reader)
    else:
        df = load(sys.stdin)

    if args.outfile:
        with open(args.outfile, "w") as writer:
            df.to_csv(writer, index=False)
    else:
        df.to_csv(sys.stdout, index=False)
```

---

## Parsing Arguments

-   Use `argparse` module to parse arguments

```{data-file="parse.py:parse_args"}
def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--infile", type=str, default=None, help="input")
    parser.add_argument("--outfile", type=str, default=None, help="output")
    return parser.parse_args()
```

---

## Loading Data

-   To load:
    -   Get all lines
    -   Split into header and body
    -   Normalize the body (i.e., adjust indentation if necessary)
    -   Create dataframe

```{data-file="parse.py:load"}
def load(reader):
    """Load messy data."""
    lines = [row for row in csv.reader(reader)]
    header, body = split(lines)
    titles, data = normalize(body)
    assert titles[0] == "site"
    return pd.DataFrame(data, columns=titles)
```

---

## Finite State Machine

-   Splitting is the hardest part
-   Manage complexity with a a [finite state machine](g:fsm)
    1.  Reading header
    2.  Searching for body
    3.  Reading body
    4.  Done
-   Use an enumeration to keep track of these

```{data-file="parse.py:state"}
class State(Enum):
    """Enumerate possible parser states."""

    HEADER = "header"
    SEARCHING = "searching"
    BODY = "body"
    DONE = "done"
```

---

## Structure

-   As we process each line
    -   Break down cases based on current state
    -   (Possibly) do something with the line
    -   Decide our next state
-   A structured way to manage complexity as parsing gets more complicated
   -   Could just use strings instead of an enum, but the latter is easy to keep track of

---

## Structure

```{data-file="parse.py:split"}
def split(rows):
    """Split header from body."""
    header, body, state = [], [], State.HEADER
    for row in rows:
        if state == State.HEADER:
            if is_empty(row):
                state = State.SEARCHING
            elif is_start_of_body(row):
                state = State.BODY
                body.append(row)
            else:
                header.append(row)

        elif state == State.SEARCHING:
            if is_start_of_body(row):
                state = State.BODY
                body.append(row)

        elif state == State.BODY:
            if is_empty(row):
                state = State.DONE
            else:
                body.append(row)

        else:
            assert state == State.DONE

    return header, body
```

---

## Normalization

-   To normalize the body, check indentation of first row
    -   Really should confirm indentation of remaining rows

```{data-file="parse.py:normalize"}
def normalize(rows):
    """Remove leading spaces from rows if necessary."""
    if rows[0][0] == "":
        rows = [r[1:] for r in rows]
    return [r.lower() for r in rows[0]], rows[1:]
```

---

## What We Have Now

<figure id="parse_call_tree">
  <img src="call_tree.svg" alt="Call tree of completed parser"/>
  <figcaption>Figure 1: Parser call tree</figcaption>
</figure>

-   Run it on our files and check the results

---

## Exercises

1.  Check that all rows of body are indented the same amount.

1.  Check that all expected columns are there.

1.  Check consistency of site name in header with site names on rows.

1.  Check longitude and latitude: what are reasonable bounds on these?

1.  Check readings: what are reasonable values for these?

1.  Were your "reasonable" bounds for the previous two exercises the same as other people's?
    How can you make them easier to discover?
    Should they be changeable from the command line?

1.  Modify the parser to take an optional filename as an argument.
    If one is provided,
    the parser reads a dataframe from that file
    and compares it to the dataframe loaded from the first file.
    How would you use this in testing?
