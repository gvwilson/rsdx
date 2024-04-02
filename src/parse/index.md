---
title: "Parse Raw Data"
tagline: "Turning messy data files into something we can process more easily."
syllabus:
-   Writing command-line tools that respect Taschuk's Rules.
-   Creating a data manifest (and why you want one).
-   Using regular expressions if you have to, but an out-of-the-box parser if one is available.
---

-   We are studying the impact of a toxic waste leak on snails on Vancouver Island
-   First step is to read data files with snail weight readings from four sample sites
-   First file looks like this

```csv
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
    -   site ID repeated
    -   observation date (we presume) in ISO YYYY-MM-DD format (we hope)
    -   longitude and latitude of the measurement (decimal degrees)
    -   the reading
-   That seems simple

[%inc naive.py %]
[%inc naive_GBY.out %]

-   Try it on the next file

[%inc naive_YOU.out %]

-   Problem is that the table of readings is indented by one column
-   Next file starts like this:

```csv
Site:,COW
Analyst:,P. Srinath

SITE,DATE,LON,LAT,READING
COW,2023-04-27,-124.04518,48.82171,106.9
COW,2023-04-27,-124.045,48.8216,81.7
…
```

-   And another one has *two* blank lines between the header and the data
-   Option 1: edit the data files
    -   Never do this
-   Option 2: copy and edit the files
    -   But it turns out each field scientist submitted dozens of files
    -   Each person was consistent, but editing them all by hand will be tedious and error-prone
-   Option 3: write a parser
    -   Follow Taschuk's Rules [%b Taschuk2017 %]
-   Main body follows 50-year-old conventions for Unix command-line tools
    -   Get command-line arguments
    -   Read from standard input or a file (processing as we read)
    -   Write to standard output or a file

[%inc parse.py pattern=func:main %]

-   Use `argparse` module to parse arguments

[%inc parse.py pattern=func:parse_args %]

-   To load:
    -   Get all lines
    -   Split into header and body
    -   Normalize the body (i.e., adjust indentation if necessary)
    -   Create dataframe

[%inc parse.py pattern=func:load %]

-   Splitting is the hardest part
-   We can be in one of four states
    -   Reading header
    -   Searching for body
    -   Reading body
    -   Done
-   Use an enumeration to keep track of these

[%inc parse.py pattern=class:State %]

-   As we process each line
    -   Break down cases based on current state
    -   (Possibly) do something with the line
    -   Decide our next state
-   A structured way to manage complexity as parsing gets more complicated
   -   Could just use strings instead of an enum, but the latter is easy to keep track of

[%inc parse.py pattern=func:split %]

-   To normalize the body, check indentation of first row
    -   Really should confirm indentation of remaining rows

[%inc parse.py pattern=func:normalize %]

-   Result

[% figure
   slug="parse_call_tree"
   img="call_tree.svg"
   alt="Call tree of completed parser"
   caption="Parser call tree"
%]

-   Run it on our files and check the results

## Exercises {: #parse-exercises}

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
