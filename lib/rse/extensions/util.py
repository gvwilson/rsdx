"""Utilities for building site."""

from datetime import datetime
from pathlib import Path
import sys
import yaml

import ark


CACHE = None
DIRECTIVES_FILE = ".ark"


def with_cache(original):
    """Make sure cache has been built before function runs."""

    def wrapped(*args, **kwargs):
        global CACHE
        if CACHE is None:
            CACHE = {
                "date": datetime.utcnow().replace(microsecond=0).isoformat(" "),
                "titles": {
                    slug: title for (slug, title) in ark.site.config["chapters"].items()
                },
            }
        return original(*args, **kwargs)

    return wrapped


def fail(msg):
    """Fail unilaterally."""
    print(msg, file="sys.stderr")
    raise AssertionError(msg)


def get_slug(node):
    """Get chapter-level slug of file."""
    return node.path[-1] if len(node.path) > 0 else "@root"


@with_cache
def get_date():
    """Get date/time."""
    return CACHE["date"]

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


def require(cond, msg):
    """Fail if condition untrue."""
    if not cond:
        fail(msg)
