"""Utilities for building site."""

from pathlib import Path
import yaml

import ark


CACHE = None
DIRECTIVES_FILE = ".ark"


def _make_cache():
    """Build the configuration cache."""
    global CACHE
    CACHE = {
        "titles": {
            slug: title for (slug, title) in ark.site.config["chapters"].items()
        }
    }


def with_cache(original):
    """Make sure cache has been built before function runs."""
    def wrapped(*args, **kwargs):
        if CACHE is None:
            _make_cache()
        return original(*args, **kwargs)
    return wrapped


def get_slug(node):
    """Get chapter-level slug of file."""
    return node.path[-1] if len(node.path) > 0 else "@root"


@with_cache
def get_title(node):
    """Get chapter/appendix title from configuration."""
    return CACHE["titles"][get_slug(node)]


def read_directives(dirname):
    """Get contents of directives file if it exists"""
    filepath = Path(dirname).joinpath(DIRECTIVES_FILE)
    if not filepath.exists():
        return {}
    with open(filepath, "r") as reader:
        return yaml.safe_load(reader) or {}
