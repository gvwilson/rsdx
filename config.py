"""Ark configuration file."""
title = "Research Software Design by Example"
slug = "rsdx"
repo = f"https://github.com/gvwilson/{slug}"
author = {
    "name": "Greg Wilson",
    "email": "gvwilson@third-bit.com",
    "site": "https://third-bit.com/",
}
lang = "en"

chapters = [
    "intro",
    "parse",
    "plugin",
    "refactor",
    "test",
    "perf",
    "lazy",
    "scale",
    "package",
    "mutate",
    "search",
    "lims",
    "website",
    "scrape",
    "serve",
    "finale",
]

appendices = [
    "license",
    "bib",
    "conduct",
    "glossary",
    "credits",
    "colophon",
]

# What to copy
copy = [
    "*.out",
    "*.png",
    "*.py",
    "*.sh",
    "*.svg",
]

# What not to copy
exclude = copy + [
    "*.css",
    "*.csv",
    "*.db",
    "*.dvc",
    "*.env",
    "*.jinja",
    "*.json",
    "*.metaflow",
    "*.mk",
    "*.pdf",
    "*.sql",
    "*.tbl",
    "*.txt",
    "*.yml",
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

# Theme information.
theme = "mccole"
src_dir = "src"
out_dir = "docs"
extension = "/"

# Enable various Markdown extensions.
markdown_settings = {
    "extensions": [
        "markdown.extensions.extra",
        "markdown.extensions.smarty",
        "pymdownx.superfences",
    ]
}

# Display values for LaTeX generation.
if __name__ == "__main__":
    import sys

    assert len(sys.argv) == 2, "Expect exactly one argument"
    if sys.argv[1] == "--order":
        print(" ".join(chapters + appendices))
    elif sys.argv[1] == "--slug":
        print(slug)
    elif sys.argv[1] == "--title":
        print(title)
    else:
        assert False, f"Unknown flag {sys.argv[1]}"
