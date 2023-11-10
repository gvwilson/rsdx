from datetime import datetime
from glob import iglob
from pathlib import Path
from shutil import copyfile

import ark

import util


def all_tasks():
    """Run all startup tasks in order."""

    _set_build_timestamp()
    _load_bibliography()
    _load_links()
    _collect_meta()
    _number_chapters()
    _append_links_to_pages()
    _copy_files()


def _append_links_to_pages():
    """Add Markdown links table to Markdown files."""

    def _visitor(node):
        if node.ext == "md":
            node.text += "\n\n" + util.make_links_table(node.text)

    ark.nodes.root().walk(_visitor)


def _collect_meta():
    """Collect metadata from all Markdown files."""

    def _visitor(node):
        if (node.ext != "md") or (not node.slug):
            return
        ark.site.config["_meta_"][node.slug] = node.meta

    ark.site.config["_meta_"] = {}
    ark.nodes.root().walk(_visitor)


def _copy_files():
    """Copy files."""
    for pat in ark.site.config["copy"]:
        src_dir = ark.site.src()
        out_dir = ark.site.out()
        pat = Path(src_dir, "**", pat)
        for src_file in iglob(str(pat), recursive=True):
            out_file = src_file.replace(src_dir, out_dir)
            Path(out_file).parent.mkdir(exist_ok=True, parents=True)
            copyfile(src_file, out_file)


def _load_bibliography():
    """Ensure bibliography is in memory."""
    ark.site.config["_bib_"] = util.read_bibliography()


def _load_links():
    """Load links file."""
    ark.site.config["_links_"] = {
        lnk["key"]: lnk for lnk in util.read_info("links.yml")
    }


def _number_chapters():
    """Number chapters."""
    ark.site.config["_number_"] = {}
    first_appendix = None
    for i, slug in enumerate(ark.site.config["chapters"]):
        if "tag" in ark.site.config["_meta_"][slug]:
            ark.site.config["_number_"][slug] = {
                "kind": "Chapter",
                "number": str(i + 1),
            }
        else:
            if first_appendix is None:
                first_appendix = i
            ark.site.config["_number_"][slug] = {
                "kind": "Appendix",
                "number": chr(ord("A") + i - first_appendix),
            }


def _set_build_timestamp():
    """Record time of build."""
    ark.site.config["_date_"] = datetime.utcnow().replace(microsecond=0).isoformat(" ")
