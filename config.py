"""Ark configuration file."""

title = "Research Software Design by Example"
repo = "https://github.com/gvwilson/rsdx"
author = "Greg Wilson"

chapters = {
    "intro": "Introduction",
    "parse": "Parse Raw Data",
    "center": "Geocoded Readings",
    "script": "Initial Script",
    "grid": "Grid Abstraction",
    "perf": "Measure Performance",
    "flow": "Task Runner",
    "lazy": "Lazy Algorithm",
    "dim": "Measure Fractal Dimension",
    "density": "Estimate Density vs. Distance",
    "test": "Testing",
    "mut": "Mutation",
    "walk": "Random Walk",
    "finale": "Conclusion",
    "license": "License",
    "bib": "Bibliography",
    "conduct": "Code of Conduct",
    "credits": "Credits",
    "docs": "Documentation",
}

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
