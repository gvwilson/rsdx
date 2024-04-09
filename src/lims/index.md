---
title: "Laboratory Information Management System"
tagline: "Ingest, manage, and summarize experimental data."
syllabus:
-   Check the existence, structure, content, and consistency of data in that order.
-   Separate quality control checks from reports.
-   Use models, views, and controllers to build interactive applications.
-   Never pass user data directly in a database query.
---

-   [%g relational_db "Relational database" %] stores data in tables
    -   Usually access with SQL or some variant of it
-   But there are also [%g document_db "document databases" %]
    -   Sometimes called [%g nosql "NoSQL" %] databases
-   We will build a (very) simple [%g lims "laboratory information management systems" %] (LIMS)
    using [TinyDB][tinydb]
-   And use [click][click] to build the command-line interface

## Roles and Permissions {: #lims-perms}

-   A user has a [%g uid "UID" %], a personal name, and a family name
-   A [%g permission "permission" %] is the right to perform some action
    -   Could give permissions directly to users…
    -   …but experience shows that this becomes unmanageable
-   Instead, create [%g role "roles" %] that are named collections of permissions and assign roles to users
    ([%t lims_perms %])

[%table slug="lims_perms" tbl="lims_perms.tbl" caption="Permissions in LIMS" %]

-   Copy data from table of personal and family names
-   First person becomes an admin, second an intern, everyone else a scientist
-   Main driver:

[%inc create_db.py pattern=func:main %]

-   Get people from SQL table using a row factory

[%inc create_db.py pattern=func:get_people %]

-   Create capabilities in TinyDB

[%inc create_db.py mark=capabilities %]
[%inc create_db.py pattern=func:create_capabilities %]

-   Resulting JSON
    -   Yes, this is really just a rectangular table stored as JSON

[%inc capabilities.json %]

-   Similar to create people and roles, e.g.:

[%inc person.json %]

## Actions {: #lims-actions}

-   Create a dataclass to represent assay data

[%inc assay_params.py pattern=class:Params %]
[%inc assay_params.py pattern=func:load_params %]

-   Then create a group of commands with click

[%inc lims.py pattern=func:cli %]

-   Now define a command to upload

[%inc lims.py pattern=func:upload %]

-   That's a lot of decorators…
-   Each `@click.option` defines a flag for the `upload` command
-   Run like this

[%inc upload.sh %]

-   Top half of `upload` loads data and checks for errors
    -   Discuss below
-   Bottom half interacts with database
-   Make sure the user exists

[%inc lims.py pattern=func:_require_exists %]

-   Get the user's capabilities

[%inc lims.py pattern=func:_get_capability %]

-   Check that the user has the required capability

[%inc lims.py pattern=func:_require_cap %]

-   *Then* upload the data

[%inc lims.py pattern=func:_upload_data %]

## Linting {: .lims-lint}

-   Take a closer look at error checking
-   First, get the data as a dataframe

[%inc lint.py pattern=func:load_file %]

-   Next, build framework for checks

[%inc lint.py pattern=func:lint_assay %]
[%inc lint.py pattern=func:lint_design %]
[%inc lint.py pattern=func:lint_single_file %]

-   Now define functions that do checks
    -   Will be picked up automatically

[%inc lint.py pattern=func:_lint_assay_data_shape %]
[%inc lint.py pattern=func:_lint_assay_machine_header %]

## Evaluation {: .lims-eval}

-   What makes this different from "commit data to version control"
    1.  Checking the data on the way in
    2.  Checking that people are authorized to add, view, or update data
-   Is it worth it?
    -   For a single person managing a small set of files: no
    -   For multiple people with many files: absolutely
