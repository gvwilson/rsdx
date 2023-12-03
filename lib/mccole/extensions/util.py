"""Utilities for building site."""

from collections import defaultdict
import markdown
from pathlib import Path
import re
import sys
import time
import yaml

import ark


# Level-1 Markdown heading.
FIRST_H1 = re.compile(r"^#\s+.+$", re.MULTILINE)

# Match inside HTML paragraph markers.
INSIDE_PARAGRAPH = re.compile(r"<p>(.+?)</p>")

# Match a reference to a footer link or a URL ref in an index entry.
MARKDOWN_FOOTER_LINK = re.compile(r"\[.*?\]\[(.+?)\]", re.MULTILINE)

# McCole directives.
MCCOLE_FILE = "mccole.yml"

# How long everything took.
TIMINGS = defaultdict(float)


def timing(func):
    """Time-recording decorator."""

    def wrapper(*args, **kwargs):
        global TIMINGS
        t_start = time.time()
        result = func(*args, **kwargs)
        TIMINGS[func.__name__] += time.time() - t_start
        return result

    return wrapper


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
    if len(node.path) == 0:
        return ""
    if node.path[-1] == "slides":
        return node.path[-2]
    return node.path[-1]


def get_slug_from_path(path):
    """Get the containing slug from the path."""
    if path.is_file():
        path = path.parent
    root = Path(ark.site.config["src_dir"]).absolute()
    if path == root:
        return ""
    while path.parent != root:
        path = path.parent
    return path.stem


def get_tag(node):
    """Get chapter tag from collected page metadata."""
    slug = get_slug(node)
    require((slug in ark.site.config["_meta_"]), f"{node} not known")
    return ark.site.config["_meta_"][slug].get("tag", None)


def get_title(node):
    """Get chapter/appendix title from collected page metadata."""
    slug = get_slug(node)
    require((slug in ark.site.config["_meta_"]), f"{node} not known")
    return ark.site.config["_meta_"][slug]["title"]


@timing
def markdownify(text, strip_p=True, with_links=False):
    """Convert Markdown to HTML."""
    extensions = ["markdown.extensions.extra", "markdown.extensions.smarty"]
    links = ark.site.config["_links_block_"]
    combined = f"{text}\n{links}" if with_links else text
    result = markdown.markdown(combined, extensions=extensions)
    if strip_p and result.startswith("<p>"):
        result = INSIDE_PARAGRAPH.match(result).group(1)
    return result


@timing
def read_bibliography():
    """Load bibliography."""
    return Path(ark.site.home(), "tmp", "bibliography.html").read_text()


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
