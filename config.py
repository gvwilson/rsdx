"""Ark configuration file."""

title = "Research Software Design by Example"
repo = "https://github.com/gvwilson/rsdx"
author = "Greg Wilson"

debug = False
do_blank = True

chapters = [
    "intro",
    "parse",
    "center",
    "script",
    "grid",
    "perf",
    "flow",
    "lazy",
    "dim",
    "density",
    "test",
    "mut",
    "walk",
    "finale",
    "license",
    "bib",
    "conduct",
    "credits",
    "syllabus",
    "docs",
]

theme = "book"

copy = [
    "*.csv",
    "*.svg",
]

exclude = copy + [
    "*.db",
    "*.dvc",
    "*.mk",
    "*.py",
    "*.tbl",
    "*~",
    ".#*",
    ".coverage",
    ".pytest_cache",
    "CODE_OF_CONDUCT.md",
    "DOCS.md",
    "LICENSE.md",
    "Makefile",
    "README.md",
    "__pycache__",
    "htmlcov",
    "pyproject.toml",
    "requirements.txt",
]

lint = {
    "disable_h2_id": ["conduct", "docs"],
}

markdown_settings = {
    "extensions": [
        "markdown.extensions.extra",
        "markdown.extensions.smarty",
        "pymdownx.superfences",
    ]
}

src_dir = "docs"
out_dir = "site"

extension = "/"
