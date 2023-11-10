"""Ark hooks."""

from fnmatch import fnmatch
from glob import iglob
from pathlib import Path
from shutil import copyfile

import ark
import util


@ark.events.register(ark.events.Event.INIT_BUILD)
def startup():
    """Launch startup tasks in order."""
    _startup_collect_meta()
    _startup_append_links_to_pages()
    _startup_copy_files()


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


def _startup_append_links_to_pages():
    """Add Markdown links table to Markdown files."""

    def _visitor(node):
        if node.ext == "md":
            node.text += "\n\n" + util.make_links_table(node.text)

    ark.nodes.root().walk(_visitor)


def _startup_collect_meta():
    """Collect metadata from all Markdown files."""

    def _visitor(node):
        if (node.ext != "md") or (not node.slug):
            return
        ark.site.config["meta"][node.slug] = node.meta

    ark.site.config["meta"] = {}
    ark.nodes.root().walk(_visitor)


def _startup_copy_files():
    """Copy files."""
    for pat in ark.site.config["copy"]:
        src_dir = ark.site.src()
        out_dir = ark.site.out()
        pat = Path(src_dir, "**", pat)
        for src_file in iglob(str(pat), recursive=True):
            out_file = src_file.replace(src_dir, out_dir)
            Path(out_file).parent.mkdir(exist_ok=True, parents=True)
            copyfile(src_file, out_file)
