"""Display key points of chapter."""

import ark
import ibis

import util


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
        f"No syllabus for {node.slug} in metadata {metadata[node.slug]}",
    )
    points = [util.markdownify(p) for p in metadata[node.slug]["syllabus"]]
    points = "\n".join([f"<li>{p}</li>" for p in points])
    return f'<ul class="keypoints">\n{points}\n</ul>'
