---
title: "A Python Package"
tagline: "Navigating the confusion of creating a simple Python package."
syllabus:
-   Creating an installable package is the best way to share your code with other people.
-   Python's packaging tools are a complex mess.
-   The first step in creating a package is to write a manifest describing its contents and how to build it.
-   Packages can be installed locally for testing purposes before being distributed.
-   Always use virtual environments when building and using packages.
---

-   Best way to distribute software and data is as a package someone can install
    -   Sadly, there still isn't support for distributing lessons that way…
-   Python's packaging tools are a complex mess
    -   That was true [over a decade ago][aosa_py_package] and has only gotten worse
-   Show how to write a basic package

-   [%g boilerplate "Boilerplate" %] files
    -   Create `README` file explaining what the package is
    -   Choose `LICENSE` that describes who can use it how
    -   Use upper case names by convention so that case-sensitive `ls` will show them first

-   Create the source code
    -   Subdirectory called `invperc` contains all source code files
    -   For us, `invperc/invperc.py` is invasion percolation and `invperc/grid.py` is the lazy grid
    -   In a subdirectory so that tests, documentation, etc. can be in the repo beside it

-   Make this a Python module
    -   Contains `__init__.py` to tell Python this is a module
    -   That file defines `__version__` variable using [%g semver "semantic versioning" %]
    -   And imports things from other files in the directory
        that we want available to users as top-level imports

[%inc invperc/__init__.py %]

-   Make it runnable
    -   Create `__main__.py` as command-line script
    -   `return 0` tells the operating system there were no errors
        -   Non-zero return code means something went wrong

[%inc invperc/__main__.py %]

-   Create `pyproject.toml` in root directory
    -   [%g toml "TOML" %] is yet another "human-readable" configuration file format

[%inc pyproject.toml %]

-   `project` section
    -   `name` of package
    -   `description` is short title
    -   `readme` is the source of the README file
    -   `authors` have names and email addresses
    -   `license` is the name of the license, not the full text
    -   `dependencies` is the packages this one needs
    -   `dynamic` says "get this value from the code itself"
-   `project.urls` section
    -   `homepage` is where to find documentation
-   `build-system` (yes, hyphenated rather than `.`-based subname)
    -   `requires` is the tools needed to *build* (not to install)
    -   `build-backend` is the tool used to create the package
    -   Copy and paste
-   `tool.setuptools.dynamic` is:
    -   A tool-specific subsection…
    -   …for the `setuptools` tool…
    -   …that provides a dynamic value flagged earlier
    -   That value is `invperc.__version__`

> -   Originally wrote `[tool.setuptools.dynamic]` as `[tools.setuptools.dynamic]`
>     -   Failed, but didn't produce an error message
>     -   Half of Python's packaging tools are there to make up for shortcomings in the other half

-   To build the package

[%inc build.sh %]

-   Lots of output
-   Produces:
    -   `invperc.egg-info` with information about package
    -   `dist/invperc-0.2.0-py3-none-any.whl` and `dist/invperc-0.2.0.tar.gz` for distribution

-   To build documentation from docstrings

[%inc docs.sh %]

-   Note: please use `pdoc` rather than `pdoc3`
    -   See [this comment by the author of `pdoc`][pdoc_vs_pdoc3] for the reasons
