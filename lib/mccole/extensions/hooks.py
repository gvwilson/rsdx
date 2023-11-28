"""Ark hooks."""

from fnmatch import fnmatch
from pathlib import Path

import ark

import startup
import util


@ark.events.register(ark.events.Event.INIT_BUILD)
def on_ini_build():
    """Launch startup tasks in order."""
    startup.all_tasks()


@ark.filters.register(ark.filters.Filter.LOAD_NODE_DIR)
def keep_dir(value, path):
    """Do not process directories excluded by parent."""
    return not _ignore(path)


@ark.filters.register(ark.filters.Filter.LOAD_NODE_FILE)
def keep_file(value, path):
    """Only process the right kinds of files."""
    return not _ignore(path)


@ark.filters.register(ark.filters.Filter.OUTPUT_FILEPATH)
def modify_slides_path(output_path, node):
    if node.get_template_list()[0] == "slides":
        return output_path.replace("/slides/index.html", "/slides.html")
    return output_path


def _ignore(path):
    """Check for pattern-based exclusion."""
    # Global exclusion.
    path = Path(path)
    config = ark.site.config.get("exclude", [])
    if any(fnmatch(path.name, pat) for pat in config):
        return True

    # Excluded by metadata in containing directory.
    slug = util.get_slug_from_path(path)
    metadata = ark.site.config["_meta_"].get(slug, {}).get("exclude", [])
    if any(fnmatch(path.name, pat) for pat in metadata):
        return True

    # No reason to exclude.
    return False
