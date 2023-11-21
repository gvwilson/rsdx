"""Ark configuration file."""

title = "Research Software Design by Example"
slug = "rsdx"
repo = f"https://github.com/gvwilson/{slug}"
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
    "measure",
    "test",
    "mut",
    "dataman",
    "service",
    "finale",
    "license",
    "bib",
    "conduct",
    "credits",
    "syllabus",
    "docs",
]

theme = "mccole"

copy = [
    "*.svg",
]

exclude = copy + [
    "*.csv",
    "*.db",
    "*.dvc",
    "*.metaflow",
    "*.mk",
    "*.pdf",
    "*.py",
    "*.sql",
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

src_dir = "src"
out_dir = "docs"

extension = "/"

# Display values for LaTeX generation.
if __name__ == "__main__":
    import sys

    assert len(sys.argv) == 2, "Expect exactly one argument"
    if sys.argv[1] == "--slug":
        print(slug)
    elif sys.argv[1] == "--title":
        print(title)
    else:
        assert False, f"Unknown flag {sys.argv[1]}"
