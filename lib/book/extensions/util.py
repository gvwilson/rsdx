"""Utilities for building site."""

from datetime import datetime
from pathlib import Path
import pybtex.database
import pybtex.plugin
import sys
import yaml

import ark

import regex


BIB_STYLE = "unsrt"
CACHE = None
DIRECTIVES_FILE = ".ark"


def with_cache(original):
    """Fill cache if not already filled."""
    def wrapped(*args, **kwargs):
        global CACHE
        if CACHE is None:
            CACHE = {
                "bib": read_bibliography(),
                "date": datetime.utcnow().replace(microsecond=0).isoformat(" "),
                "links": {lnk["key"]: lnk for lnk in read_info("links.yml")},
                "titles": {slug: title for (slug, title) in ark.site.config["chapters"].items()},
            }
        return original(*args, **kwargs)
    return wrapped


def fail(msg):
    """Fail unilaterally."""
    print(msg, file=sys.stderr)
    sys.exit(1)


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


@with_cache
def make_links_table(text):
    """Make a table of links for inclusion in Markdown."""
    used = {m.group(1) for m in regex.MARKDOWN_FOOTER_LINK.finditer(text)}
    table = CACHE["links"]
    return "\n".join([f"[{key}]: {table[key]['url']}" for key in table if key in used])


def read_bibliography():
    """Load bibliography."""
    filename = Path(ark.site.home(), "info", "bibliography.bib")
    try:
        raw = pybtex.database.parse_file(filename)
        style_name = ark.site.config.get(BIB_STYLE, None)
        style = pybtex.plugin.find_plugin("pybtex.style.formatting", style_name)()
        styled_bib = style.format_bibliography(raw)
        return styled_bib
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
