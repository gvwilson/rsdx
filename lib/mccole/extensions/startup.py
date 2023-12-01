from datetime import datetime
from glob import glob
from pathlib import Path
from shutil import copyfile

import ark
import shortcodes
import yaml

import util

CONFIG_LINK_KEYS = ["title", "slug", "website", "repo", "author"]


def all_tasks():
    """Run all startup tasks in order."""

    _set_build_timestamp()
    _load_bibliography()
    _load_links()
    _collect_meta()
    _number_contents()
    _collect_targets()
    _append_links_to_pages()
    _copy_files()


@util.timing
def _append_links_to_pages():
    """Add Markdown links table to Markdown files."""

    def _visitor(node):
        if (node.ext == "md") or (node.slug == "slides"):
            node.text += "\n\n" + ark.site.config["_links_block_"]

    ark.nodes.root().walk(_visitor)


@util.timing
def _collect_meta():
    """Collect metadata from mccole.yml files."""
    ark.site.config["_meta_"] = {
        slug: yaml.safe_load(
            Path(ark.site.config["src_dir"], slug, util.MCCOLE_FILE).read_text()
        )
        for slug in ark.site.config["contents"]
    }


@util.timing
def _collect_targets():
    """Collect targets of numbered cross-references."""

    def _collect_figures(pargs, kwargs, extra):
        util.require(
            "slug" in kwargs,
            f"Bad 'figure' shortcode in {extra['filename']} with {pargs} and {kwargs}",
        )
        extra["figures"].append(kwargs["slug"])

    def _collect_tables(pargs, kwargs, extra):
        util.require(
            "slug" in kwargs,
            f"Bad 'table' shortcode in {extra['filename']} with {pargs} and {kwargs}",
        )
        extra["tables"].append(kwargs["slug"])

    def _visitor(node):
        if _do_not_collect(node, include_slides=True):
            return

        collected = {"filename": node.filepath, "figures": [], "tables": []}
        parser.parse(node.text, collected)
        node_slug = util.get_slug(node)
        if node_slug not in collector:
            collector[node_slug] = {"figures": {}, "tables": {}}
        collector[node_slug]["figures"].update(
            {fig_slug: i + 1 for i, fig_slug in enumerate(collected["figures"])}
        )
        collector[node_slug]["tables"].update(
            {tbl_slug: i + 1 for i, tbl_slug in enumerate(collected["tables"])}
        )

    parser = shortcodes.Parser(inherit_globals=False, ignore_unknown=True)
    parser.register(_collect_figures, "figure")
    parser.register(_collect_tables, "table")
    collector = {}
    ark.nodes.root().walk(_visitor)
    ark.site.config["_figures_"] = {}
    ark.site.config["_tables_"] = {}
    for slug, seen in collector.items():
        for key, number in seen["figures"].items():
            ark.site.config["_figures_"][key] = number
        for key, number in seen["tables"].items():
            ark.site.config["_tables_"][key] = number


@util.timing
def _copy_files():
    """Copy files from source directories (not recursive)."""
    for pat in ark.site.config["copy"]:
        src_dir = ark.site.src()
        out_dir = ark.site.out()
        pat = Path(src_dir, "*", pat)
        for src_file in glob(str(pat)):
            out_file = src_file.replace(src_dir, out_dir)
            Path(out_file).parent.mkdir(exist_ok=True, parents=True)
            copyfile(src_file, out_file)


@util.timing
def _do_not_collect(node, include_slides):
    """Do not collect data from node (root page or slides)."""

    # Root page.
    if not node.slug:
        return True

    # Markdown file.
    if node.ext == "md":
        return False

    # Slides.
    if (node.slug == "slides") and include_slides:
        return False

    # Nope.
    return True


@util.timing
def _load_bibliography():
    """Ensure bibliography is in memory."""
    ark.site.config["_bib_"] = util.read_bibliography()


@util.timing
def _load_links():
    """Load links file."""
    links = util.read_info("links.yml")
    ark.site.config["_links_"] = {lnk["key"]: lnk for lnk in links}
    ark.site.config["_links_block_"] = "\n".join(
        f"[{key}]: {value['url']}" for key, value in ark.site.config["_links_"].items()
    )


@util.timing
def _number_contents():
    """Number chapters and appendices."""
    chapters = {
        slug: {"kind": "Chapter", "number": str(i + 1)}
        for i, slug in enumerate(ark.site.config["chapters"])
    }
    appendices = {
        slug: {"kind": "Appendix", "number": chr(ord("A") + i)}
        for i, slug in enumerate(ark.site.config["appendices"])
    }
    ark.site.config["_number_"] = chapters | appendices


@util.timing
def _set_build_timestamp():
    """Record time of build."""
    ark.site.config["_date_"] = datetime.utcnow().replace(microsecond=0).isoformat(" ")
