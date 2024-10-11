# A Laboratory Information Management System

-   [Relational](g:relational_db)abase" %] stores data in tables
    -   Usually access with SQL or some variant of it
-   But there are also [document](g:document_db)abases" %]
    -   Sometimes called [NoSQL](g:nosql) databases
-   We will build a (very) simple [laboratory](g:lims)ormation management systems" %] (LIMS)
    using [TinyDB][tinydb]
-   And use [click][click] to build the command-line interface

## Roles and Permissions {: #lims-perms}

-   A user has a [UID](g:uid), a personal name, and a family name
-   A [permission](g:permission) is the right to perform some action
    -   Could give permissions directly to users…
    -   …but experience shows that this becomes unmanageable
-   Instead, create [roles](g:role) that are named collections of permissions and assign roles to users

| Role      | Capability | Scope |
| --------- | ---------- | ----- |
| admin     | view       | all   |
| admin     | upload     | own   |
| admin     | validate   | all   |
| scientist | view       | all   |
| scientist | upload     | own   |
| intern    | view       | own   |

-   Copy data from table of personal and family names
-   First person becomes an admin, second an intern, everyone else a scientist
-   Main driver:

[%inc create_db.py keep=main %]

-   Get people from SQL table using a row factory

[%inc create_db.py keep=get_people %]

-   Create capabilities in TinyDB

[%inc create_db.py keep=capabilities %]
[%inc create_db.py keep=create_capabilities %]

-   Resulting JSON
    -   Yes, this is really just a rectangular table stored as JSON

[%inc capabilities.json %]

-   Similar to create people and roles, e.g.:

[%inc person.json %]

## Actions {: #lims-actions}

-   Create a dataclass to represent assay data

[%inc assay_params.py keep=params %]
[%inc assay_params.py keep=load_params %]

-   Then create a group of commands with click

[%inc lims.py keep=cli %]

-   Now define a command to upload

[%inc lims.py keep=upload %]

-   That's a lot of decorators…
-   Each `@click.option` defines a flag for the `upload` command
-   Run like this

[%inc upload.sh %]

-   Top half of `upload` loads data and checks for errors
    -   Discuss below
-   Bottom half interacts with database
-   Make sure the user exists

[%inc lims.py keep=require_exists %]

-   Get the user's capabilities

[%inc lims.py keep=get_capability %]

-   Check that the user has the required capability

[%inc lims.py keep=require_cap %]

-   *Then* upload the data

[%inc lims.py keep=upload_data %]

## Linting {: .lims-lint}

-   Take a closer look at error checking
-   First, get the data as a dataframe

[%inc lint.py keep=load_file %]

-   Next, build framework for checks

[%inc lint.py keep=lint_assay %]
[%inc lint.py keep=lint_design %]
[%inc lint.py keep=lint_single_file %]

-   Now define functions that do checks
    -   Will be picked up automatically

[%inc lint.py keep=lint_assay_data_shape %]
[%inc lint.py keep=lint_assay_machine_header %]

## Evaluation {: .lims-eval}

-   What makes this different from "commit data to version control"
    1.  Checking the data on the way in
    2.  Checking that people are authorized to add, view, or update data
-   Is it worth it?
    -   For a single person managing a small set of files: no
    -   For multiple people with many files: absolutely
