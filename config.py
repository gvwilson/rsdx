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
# plausible = "gvwilson.github.io/rsdx"

chapters = [
    "intro",
    "parse",
    "plugin",
    "cleanup",
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

# Files and directories to skip
exclude = {
    "lims/assays",
    "lims/designs",
    "website/site",
    "serve/static",
    "serve/templates",
    "package/LICENSE.md",
    "package/README.md",
    "package/invperc",
}

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

# Show theme.
if __name__ == "__main__":
    print(theme)
