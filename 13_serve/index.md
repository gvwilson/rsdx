# A Web Service

## Getting Data {: #serve-data}

-   Assay database from [the LIMS chapter](../10_lims/index.md)
    -   `staff`
    -   `experiment`
    -   `performed`
    -   `plate`
    -   `invalidated`
-   Use [sqlite3][sqlite3] module directly
    -   Exercise: convert to [SQLModel][sqlmodel]
-   [MVC](g:mvc) design separates [model](g:model), [controller](g:controller), and [view](g:view)
    -   Model is data storage
    -   Controller is the verbs
    -   View is the display
-   Model functions:
    -   `get_all` to get all records (but *not* 1-1 with database records)
    -   `get_count` to count records of a particular type
    -   `get_plate_filename` to turn a plate ID into an assay filename

[%inc model.py keep=get_count %]

## Controller {: #serve-server}

-   Use [Flask][flask]
    -   Define a function to handle a request to a particular URL
    -   Use a decorator to [route](g:route) appropriate requests to it

[%inc server.py keep=index %]

-   Run from the command line

[%inc run_server.sh %]
[%inc run_server.out %]

-   Go to port 5000

[% figure
   id="serve_home_page"
   src="serve_home_page.svg"
   alt="screenshot of data server home page"
   caption="Home page of data server"
%]

## Templates {: #serve-template}

-   `render_template` looks in the `templates` directory for `index.html`

[%inc templates/index.html %]

-   This template [extends](g:extend_template) `base.html`

[%inc templates/base.html %]
