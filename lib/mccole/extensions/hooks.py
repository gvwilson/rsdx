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
    return not _ignore(Path(path))


@ark.filters.register(ark.filters.Filter.LOAD_NODE_FILE)
def keep_file(value, path):
    """Only process the right kinds of files."""
    return not _ignore(Path(path))


def _ignore(path):
    """Check for pattern-based exclusion."""
    config = ark.site.config.get("exclude", [])
    directives = util.read_directives(Path(path).parent).get("exclude", [])
    result = any(fnmatch(path.name, pat) for pat in config + directives)
    return result
