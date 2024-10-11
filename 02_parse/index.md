# Parsing Raw Data

## The Problem

-   We are studying the impact of toxic waste on snails on Vancouver Island
-   First step is to read data files with snail weight readings from four sample sites
-   But the files are formatted inconsistently

---

## The Data

-   First file looks like this

[%inc GBY.csv %]

-   First row has only two columns (one of which includes the site ID, which we can check against the file name)
-   After that we have five nicely-formatted columns

---

## Just Read It

-   That seems simple

[%inc naive.py %]
[%inc naive_GBY.out %]

---

## But…

-   Try it on the next file

[%inc naive_YOU.out %]

-   Problem is that the readings are indented by one column

---

## And…

-   Next file has a blank line between header and readings

[%inc COW.csv %]

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

[%inc parse.py keep=main %]

---

## Parsing Arguments

-   Use `argparse` module to parse arguments

[%inc parse.py keep=parse_args %]

---

## Loading Data

-   To load:
    -   Get all lines
    -   Split into header and body
    -   Normalize the body (i.e., adjust indentation if necessary)
    -   Create dataframe

[%inc parse.py keep=load %]

---

## Finite State Machine

-   Splitting is the hardest part
-   Manage complexity with a a [finite](g:fsm)te machine" %]
    1.  Reading header
    2.  Searching for body
    3.  Reading body
    4.  Done
-   Use an enumeration to keep track of these

[%inc parse.py keep=state %]

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

[%inc parse.py keep=split %]

---

## Normalization

-   To normalize the body, check indentation of first row
    -   Really should confirm indentation of remaining rows

[%inc parse.py keep=normalize %]

---

## What We Have Now

[% figure
   id="parse_call_tree"
   src="call_tree.svg"
   alt="Call tree of completed parser"
   caption="Parser call tree"
%]

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
