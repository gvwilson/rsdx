"""Utilities for building site."""

from datetime import datetime
from pathlib import Path
import pybtex.database
import pybtex.plugin
import sys
import yaml

import ark

import regex


DIRECTIVES_FILE = ".ark"


def fail(msg):
    """Fail unilaterally."""
    print(msg, file=sys.stderr)
    sys.exit(1)


def get_slug(node):
    """Get chapter-level slug of file."""
    return node.path[-1] if len(node.path) > 0 else "@root"


def get_date():
    """Get date/time."""
    return CACHE["date"]


def get_title(node):
    """Get chapter/appendix title from configuration."""
    return CACHE["titles"][get_slug(node)]


def make_links_table(text):
    """Make a table of links for inclusion in Markdown."""
    used = {m.group(1) for m in regex.MARKDOWN_FOOTER_LINK.finditer(text)}
    table = CACHE["links"]
    return "\n".join([f"[{key}]: {table[key]['url']}" for key in table if key in used])


def read_bibliography():
    """Load bibliography."""
    filename = Path(ark.site.home(), "info", "bibliography.bib")
    try:
        return pybtex.database.parse_file(filename)
    except FileNotFoundError:
        fail(f"Unable to read bibliography {filename}")
    except pybtex.exceptions.PybtexError:
        fail(f"Unable to parse bibliography {filename}")


def read_directives(dirname):
    """Get contents of directives file if it exists"""
    filepath = Path(dirname).joinpath(DIRECTIVES_FILE)
    if not filepath.exists():
        return {}
    return yaml.safe_load(filepath.read_text()) or {}


def read_info(filename):
    """Read YAML file from project info directory."""
    filepath = Path(ark.site.home(), "info", filename)
    return yaml.safe_load(filepath.read_text()) or {}


def require(cond, msg):
    """Fail if condition untrue."""
    if not cond:
        fail(msg)


CACHE = {
    "bib": read_bibliography(),
    "date": datetime.utcnow().replace(microsecond=0).isoformat(" "),
    "links": {lnk["key"]: lnk for lnk in read_info("links.yml")},
    "titles": {slug: title for (slug, title) in ark.site.config["chapters"].items()},
}
