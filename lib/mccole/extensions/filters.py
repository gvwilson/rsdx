"""Page elements."""

import ark
import ibis

import util
from glossary import glossary_ref


@ibis.filters.register("is_chapter")
def is_chapter(node):
    """Is this a chapter node (vs. appendix)?"""
    return node.slug and node.slug in ark.site.config["chapters"]


@ibis.filters.register("keypoints")
def keypoints(node):
    """Construct key points listing for chapter."""
    if (not node.slug) or (node.slug not in ark.site.config["chapters"]):
        return ""
    metadata = ark.site.config["_meta_"]
    util.require(
        node.slug in metadata,
        f"Slug {node.slug} not in metadata",
    )
    util.require(
        "syllabus" in metadata[node.slug],
        f"No syllabus for {node.slug} in metadata",
    )
    points = [util.markdownify(p) for p in metadata[node.slug]["syllabus"]]
    points = "\n".join([f"<li>{p}</li>" for p in points])
    return f'<ul class="keypoints">\n{points}\n</ul>'


@ibis.filters.register("nav_next")
def nav_next(node):
    """Create next-page link."""
    return _nav_link(node, "next")


@ibis.filters.register("nav_prev")
def nav_prev(node):
    """Create previous-page link."""
    return _nav_link(node, "prev")


@ibis.filters.register("tagline")
def tagline(node):
    """Insert chapter tagline (must exist)."""
    util.require(
        node.slug in ark.site.config["chapters"],
        f"bad tagline request: {node.path} is not a chapter",
    )
    metadata = ark.site.config["_meta_"]
    util.require(
        node.slug in metadata,
        f"no metadata for {node.path}",
    )
    return util.markdownify(metadata[node.slug].get("tagline"))


@ibis.filters.register("termdefs")
def termdefs(node):
    """Construct list of defined terms."""
    if (not node.slug) or (node.slug not in ark.site.config["chapters"]):
        return ""
    keys = ark.site.config["_terms_"].get(node.slug, None)
    if not keys:
        return ""
    lang = ark.site.config["lang"]
    glossary = {g["key"]: g for g in util.load_glossary()}
    terms = [glossary_ref([key, glossary[key][lang]["term"]], {}, node) for key in sorted(keys)]
    terms = ", ".join(terms)
    return f'<p class="terms">{util.kind('defined')}: \n{terms}\n</p>'


def _nav_link(node, kind):
    """Generate previous/next page links."""
    if not node.slug:
        return ""
    contents = ark.site.config["chapters"] + ark.site.config["appendices"]
    try:
        where = contents.index(node.slug)
    except ValueError:
        util.fail(f"unknown slug {node.slug} in {node.path}")
    if kind == "prev":
        if where == 0:
            return ""
        return f'<a href="@root/{contents[where - 1]}/">&lArr;</a>'
    elif kind == "next":
        if where == (len(contents) - 1):
            return ""
        return f'<a href="@root/{contents[where + 1]}/">&rArr;</a>'
    else:
        util.fail(f"Unknown nav link type '{kind}' in {node.path}")
