"""Filters for use in template expansion."""

import ark
import ibis
import util


@ibis.filters.register("is_chapter")
def is_chapter(node):
    """Is this a chapter node (vs. appendix)?"""
    return (not is_root(node)) and (util.get_tag(node) is not None)


@ibis.filters.register("is_root")
def is_root(node):
    """Is this the root node?"""
    return len(node.path) == 0


@ibis.filters.register("not_root")
def not_root(node):
    """Is this _not_ the root node?"""
    return not is_root(node)


@ibis.filters.register("part_tag")
def part_tag(node):
    """Insert chapter tag (must exist)."""
    tag = util.get_tag(node)
    util.require(tag is not None, f"{node.slug} does not have tag")
    return tag


@ibis.filters.register("part_title")
def part_title(node):
    """Insert chapter title."""
    return util.get_title(node)


@ibis.filters.register("syllabus")
def syllabus(node):
    """Format syllabus of chapter."""
    meta = ark.site.config["_meta_"][node.slug]
    util.require("syllabus" in meta, f"No syllabus for {node.slug}")
    items = "\n".join(
        [f"<li>{util.markdownify(s, True)}</li>" for s in meta["syllabus"]]
    )
    return f'<ul class="syllabus">\n{items}\n</ul>'
