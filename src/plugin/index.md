-   Research data may come from files, databases, websites, and many other sources
-   Instead of adding code to a program to handle each one,
    use a [%g plugin_architecture "plugin architecture" %]
    that loads data handlers dynamically
-   Lets users extend the program without modifying its internals
-   Work backward from configuration file
    -   File type and parameter(s) it needs

[%inc plugins.json %]

## Generic Program {: #plugin-generic}

-   Table structure

[% figure
   slug="plugin_table_structure"
   img="table_structure.svg"
   alt="Structure of survey tables"
   caption="Survey table structure"
%]

-   Write `main`
    -   If the file type is X, load `plugin_X` as a module
    -   Then call the `read_data` function in that module
    -   A [%g contract "contract" %] between the program and its plugins

[%inc display.py pattern=func:main %]

-   Result from each `read_data` is a list of tables
    -   Load all available examples to [%g cross_validation "cross validate" %]

-   Parsing command-line arguments is simple

[%inc display.py pattern=func:parse_args %]

-   Checking tables against each other
    -   Do they have the same keys?
    -   Do they have the same number of values for each key?

[%inc display.py pattern=func:check %]

-   Have one more function to generate a plot like [%f plugin-example %]

[% figure
   slug="plugin-example"
   img="./COW.svg"
   caption="Sample distribution at COW site."
   alt="Geographical map of sample distributions around COW site."
%]

## Handling CSV {: #plugin-csv}

-   Plugin to handle CSV is the simplest
    -   Read all the files in the directory using Pandas

[%inc plugin_csv.py %]

-   Combine

[%inc util.py pattern=func:combine_with_pandas %]

## Handling Databases {: #plugin-db}

-   What if data is in a database?
-   Pandas can read directly given a SQL query
-   The simple query

[%inc util.py mark=query %]

-   The code

[%inc plugin_sql.py pattern=func:read_data %]

-   The more complex query to find the center

[%inc plugin_sql.py mark=query %]

## Object-Relational Mapper {: #plugin-orm}

-   Use [SQLModel][sqlmodel] [%g orm "object-relational mapper" %] (ORM)
    -   Define classes using [%g type_annotation "type annotations" %]
    -   ORM maps these to database columns
-   Hard (odd) part is inter-table relationships
    -   And making sense of error messages

[%inc plugin_sqlmodel.py pattern=class:Sites %]

[%inc plugin_sqlmodel.py pattern=class:Surveys %]

[%inc plugin_sqlmodel.py pattern=class:Samples %]

-   With this, the `read_data` function is:

[%inc plugin_sqlmodel.py pattern=func:read_data %]

## Exercises {: #plugin-exercises}

1.  Calculate centers using aggregation in ORM.
