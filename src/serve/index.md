---
title: "A Web Service"
tagline: "Build a small web server to display plate data."
abstract: >
    As a counterpart to the previous lesson,
    this one shows how web servers handle requests and generate dynamic HTML pages.
    Understanding how this works will help research software engineers
    design services of their own
    and debug them when things go wrong.
syllabus:
-   Routing HTTP requests to functions.
-   Separating routing from model.
-   Creating HTML pages from Jinja templates.
-   Serving static files (and what that means).
-   The difference between data as HTML and data for machine consumption.
---

## Getting Data {: #serve-data}

-   Assay database from [%x lims %]
    -   `staff`
    -   `experiment`
    -   `performed`
    -   `plate`
    -   `invalidated`
-   Use [sqlite3][sqlite3] module directly
    -   Exercise: convert to [SQLModel][sqlmodel]
-   [%g mvc "MVC" %] design separates [%g model "model" %], [%g controller "controller" %], and [%g view "view" %]
    -   Model is data storage
    -   Controller is the verbs
    -   View is the display
-   Model functions:
    -   `get_all` to get all records (but *not* 1-1 with database records)
    -   `get_count` to count records of a particular type
    -   `get_plate_filename` to turn a plate ID into an assay filename

[%inc model.py pattern=func:get_count %]

## Controller {: #serve-server}

-   Use [Flask][flask]
    -   Define a function to handle a request to a particular URL
    -   Use a decorator to [%g route "route" %] appropriate requests to it

[%inc server.py mark=index %]

-   Run from the command line

[%inc run_server.sh %]
[%inc run_server.out %]

-   Go to port 5000 ([%f serve_home_page %])

[% figure
   slug="serve_home_page"
   img="serve_home_page.svg"
   alt="screenshot of data server home page"
   caption="Home page of data server"
%]

## Templates {: #serve-template}

-   `render_template` looks in the `templates` directory for `index.html`

[%inc templates/index.html %]

-   This template [%g extend_template "extends" %] `base.html`

[%inc templates/base.html %]
