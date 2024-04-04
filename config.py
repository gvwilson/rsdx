"""Ark configuration file."""
title = "Research Software Design by Example"
slug = "rsdx"
repo = f"https://github.com/gvwilson/{slug}"
site = f"https://gvwilson.github.io/{slug}/"
author = {
    "name": "Greg Wilson",
    "email": "gvwilson@third-bit.com",
    "site": "https://third-bit.com/",
}
lang = "en"
highlight = "tango.css"

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
    "conduct",
    "contrib",
    "bib",
    "glossary",
    "author",
    "colophon",
]

# Files to copy
copy = [
    "*.out",
    "*.png",
    "*.py",
    "*.sh",
    "*.svg",
]

# Directories to skip
exclude = [
    "website/res",
    "website/inc",
    "website/lib",
    "website/src",
    "serve/static",
    "serve/templates",
    "package/invperc",
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
