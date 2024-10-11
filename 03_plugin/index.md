# A Plugin Architecture

## The Problem

-   Research data may come from files, databases, websites, and many other sources
-   Instead of adding code to a program to handle each one,
    use a [plugin](g:plugin_architecture)hitecture" %]
    to load data handlers dynamically
-   Lets users extend the program without modifying its internals
-   Work backward from configuration file that defines plugin type and its parameters

[%inc plugins.json %]

---

## Our Data

[% figure
   id="plugin_table_structure"
   src="table_structure.svg"
   alt="Structure of survey tables"
   caption="Survey table structure"
%]

-   Each *site* has a [primary](g:primary_key)" %] and longitude/latitude
-   Each *survey* has a primary key, a site identifier ([foreign](g:foreign_key)" %]) and a date
-   Each sample has a site ID foreign key, longitude/latitude, and a reading

---

## Getting Started

-   Write `main`
    -   If the file type is X, load `plugin_X` as a module
    -   Then call the `read_data` function in that module
    -   A [contract](g:contract) between the program and its plugins

[%inc display.py keep=main %]

-   Result from each `read_data` is a list of tables
    -   Load all available examples to [cross](g:cross_validation)idate" %]

---

## Command Line

-   Parsing command-line arguments is simple

[%inc display.py keep=parse_args %]

---

## Checking

-   Checking tables against each other
    -   Do they have the same keys?
    -   Do they have the same number of values for each key?

[%inc display.py keep=check %]

---

## Display

[% figure
   id="plugin-example"
   src="./COW.svg"
   caption="Sample distribution at COW site."
   alt="Geographical map of sample distributions around COW site."
%]

---

## Handling CSV

-   Plugin to handle CSV is the simplest
    -   Read all the files in the directory using Pandas

[%inc plugin_csv.py keep=read_data %]

-   Concatenate all the tables

[%inc util.py keep=combine_with_pandas %]

---

## Handling Databases

-   Pandas can read directly given a SQL query
-   The simple query

[%inc util.py keep=query %]

---

## Handling Databases

-   The code

[%inc plugin_sql.py keep=read_data %]

---

## Finding Centers

-   The query is more complex, but the code to run it is the same

[%inc plugin_sql.py keep=query %]

---

## Object-Relational Mapper

-   Use [SQLModel][sqlmodel] [object](g:orm)ational mapper" %] (ORM)
    -   Define classes using [type](g:type_annotation)otations" %]
    -   ORM maps these to database columns
-   Hard (odd) part is inter-table relationships
    -   And making sense of error messages

[%inc plugin_sqlmodel.py keep=sites %]

[%inc plugin_sqlmodel.py keep=surveys %]

---

## Reading With an ORM

-   With this, the `read_data` function is:

[%inc plugin_sqlmodel.py keep=read_data %]

---

## Exercises

1.  Calculate centers using aggregation in ORM.
