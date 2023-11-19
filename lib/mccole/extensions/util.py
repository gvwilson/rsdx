"""Utilities for building site."""

import markdown
from pathlib import Path
import pybtex.database
import pybtex.plugin
import sys
import yaml

import ark

import regex
import util


BIB_STYLE = "unsrt"
DIRECTIVES_FILE = ".ark"


def debug(msg):
    """Report if debugging turned on."""
    if ark.site.config.get("debug", False):
        print(msg)


def fail(msg):
    """Fail unilaterally."""
    print(msg, file=sys.stderr)
    sys.exit(1)


def get_slug(node):
    """Get chapter-level slug of file."""
    return node.path[-1] if len(node.path) > 0 else "@root"


def get_tag(node):
    """Get chapter tag from collected page metadata."""
    util.require((node.slug in ark.site.config["_meta_"]), f"{node} not known")
    return ark.site.config["_meta_"][node.slug].get("tag", None)


def get_title(node):
    """Get chapter/appendix title from collected page metadata."""
    util.require((node.slug in ark.site.config["_meta_"]), f"{node} not known")
    return ark.site.config["_meta_"][node.slug]["title"]


def make_links_table(text):
    """Make a table of links for inclusion in Markdown."""
    used = {m.group(1) for m in regex.MARKDOWN_FOOTER_LINK.finditer(text)}
    table = ark.site.config["_links_"]
    return "\n".join([f"[{key}]: {table[key]['url']}" for key in table if key in used])


def markdownify(text, strip_paragraph=False):
    """Convert to Markdown."""
    extensions = ["markdown.extensions.extra", "markdown.extensions.smarty"]
    result = markdown.markdown(text, extensions=extensions)
    if strip_paragraph and result.startswith("<p>"):
        result = result[3:-4]  # remove trailing '</p>' as well
    return result


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


def read_file(node, filename, kind):
    """Load a file as text."""
    filepath = Path(Path(node.filepath).parent, filename)
    require(filepath.exists(), f"Missing {kind} file {filename} from {node}")
    return filepath.read_text()


def read_info(filename):
    """Read YAML file from project info directory."""
    filepath = Path(ark.site.home(), "info", filename)
    return yaml.safe_load(filepath.read_text()) or {}


def require(cond, msg):
    """Fail if condition untrue."""
    if not cond:
        fail(msg)


def require_file(node, filename, kind):
    """Require that a file exists."""
    filepath = Path(Path(node.filepath).parent, filename)
    require(filepath.exists(), f"Missing {kind} file {filename} from {node}")
