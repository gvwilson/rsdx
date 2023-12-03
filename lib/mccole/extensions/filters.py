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


@ibis.filters.register("is_slides")
def is_slides(node):
    """Is this a slides node?"""
    return node.get_template_list()[0] == "slides"


@ibis.filters.register("link_next")
def link_next(node):
    """Create next-page link."""
    return _link_nav(node, "next")


@ibis.filters.register("link_prev")
def link_prev(node):
    """Create previous-page link."""
    return _link_nav(node, "prev")


@ibis.filters.register("not_root")
def not_root(node):
    """Is this _not_ the root node?"""
    return not is_root(node)


@ibis.filters.register("part_tag")
def part_tag(node):
    """Insert chapter tag (must exist)."""
    tag = util.get_tag(node)
    util.require(tag is not None, f"{node.path} does not have tag")
    return util.markdownify(tag, with_links=True)


@ibis.filters.register("part_title")
def part_title(node):
    """Insert chapter title."""
    return util.get_title(node)


@ibis.filters.register("slug")
def slug(node):
    """Insert node slug."""
    return util.get_slug(node)


@ibis.filters.register("syllabus")
def syllabus(node):
    """Format syllabus of chapter."""
    slug = util.get_slug(node)
    meta = ark.site.config["_meta_"][slug]
    util.require("syllabus" in meta, f"No syllabus for {slug}")
    items = "\n".join(
        [f"<li>{util.markdownify(s, with_links=True)}</li>" for s in meta["syllabus"]]
    )
    return f'<ul class="syllabus">\n{items}\n</ul>'


def _link_nav(node, kind):
    """Generate previous/next page links."""
    slug = util.get_slug(node)
    if not slug:
        return ""
    contents = ark.site.config["contents"]
    try:
        where = contents.index(slug)
    except ValueError:
        util.fail(f"slug {slug} not found in contents")
    if kind == "prev":
        if where == 0:
            return ""
        return f'<a href="@root/{contents[where - 1]}/">&lArr;</a>'
    elif kind == "next":
        if where == (len(contents) - 1):
            return ""
        return f'<a href="@root/{contents[where + 1]}/">&rArr;</a>'
    else:
        util.fail(f"Unknown nav link type '{kind}'")
