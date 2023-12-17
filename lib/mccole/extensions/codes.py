"""Ark shortcodes."""

from pathlib import Path

import ark
import shortcodes
import textwrap
import yaml

import util


@shortcodes.register("b")
@util.timing
def bibliography_ref(pargs, kwargs, node):
    """Handle [%b key1 key2 %] biblography references."""
    util.require(
        (len(pargs) > 0) and (not kwargs),
        f"Bad 'b' shortcode with {pargs} and {kwargs} in {node}",
    )
    base = "@root/bib"
    links = [f'<a class="bib-ref" href="{base}/#{k}">{k}</a>' for k in pargs]
    links = ", ".join(links)
    return f'<span class="bib-ref">[{links}]</span>'


@shortcodes.register("bibliography")
@util.timing
def bibliography(pargs, kwargs, node):
    """Handle [% bibliography %] shortcode."""
    util.require(
        (not pargs) and (not kwargs),
        f"Bad 'bibliography' shortcode with {pargs} and {kwargs} in {node}",
    )
    return Path(ark.site.home(), "tmp", "bibliography.html").read_text()


@shortcodes.register("date")
@util.timing
def date(pargs, kwargs, node):
    """Handle [% date %] shortcode."""
    util.require(
        (not pargs) and (not kwargs),
        f"Bad 'date' shortcode with {pargs} and {kwargs}",
    )
    return ark.site.config["_date_"]


@shortcodes.register("f")
@util.timing
def figure_ref(pargs, kwargs, node):
    """Handle [%f slug %] figure reference shortcodes."""
    util.require((len(pargs) == 1) and (not kwargs), f"Bad 'f' shortcode in {node}")
    slug = pargs[0]
    known = ark.site.config["_figures_"]
    util.require(slug in known, f"Unknown figure slug {slug} in {node}")
    return f'<a class="fig-ref" href="#{slug}">Figure&nbsp;{known[slug]}</a>'


@shortcodes.register("figure")
@util.timing
def figure_def(pargs, kwargs, node):
    """Handle figure definition."""
    allowed = {"cls", "scale", "slug", "img", "alt", "caption"}
    util.require(
        (not pargs) and allowed.issuperset(kwargs.keys()),
        f"Bad 'figure' shortcode {pargs} and {kwargs} in {node}",
    )

    cls = kwargs.get("cls", None)
    cls = f' class="{cls}"' if cls is not None else ""

    scale = kwargs.get("scale", None)
    scale = f' width="{scale}"' if scale is not None else ""

    slug = kwargs["slug"]
    img = kwargs["img"]
    alt = util.markdownify(kwargs["alt"])
    caption = util.markdownify(kwargs["caption"])

    util.require_file(node, img, "figure")
    known = ark.site.config["_figures_"]

    label = f"Figure&nbsp;{known[slug]}"
    body = f'<img src="./{img}" alt="{alt}"{scale}/>'
    caption = f'<figcaption markdown="1">{label}: {caption}</figcaption>'
    return f'<figure id="{slug}"{cls}>\n{body}\n{caption}\n</figure>'


@shortcodes.register("fixme")
@util.timing
def fixme(pargs, kwargs, node):
    """Handle [% fixme 'item' ... %] shortcode."""
    util.require(
        (len(pargs) > 0) and (not kwargs),
        f"Bad 'fixme' shortcode with {pargs} and {kwargs}",
    )
    if len(pargs) == 1:
        return f'<span class="fixme" markdown="1">{pargs[0]}</span>'
    items = "\n".join(f"-   {x.strip()}" for x in pargs)
    return f'<div class="fixme" markdown="1">\n{items}\n</div>'


@shortcodes.register("image")
@util.timing
def image(pargs, kwargs, node):
    """Handle image."""
    allowed = {"src", "alt", "width"}
    util.require(
        (not pargs) and allowed.issuperset(kwargs.keys()),
        f"Bad 'image' shortcode {pargs} and {kwargs} in {node}",
    )
    src = kwargs["src"]
    alt = util.markdownify(kwargs["alt"])
    width = kwargs.get("width", None)

    util.require_file(node, src, "image")
    width = "" if (width is None) else f' width="{width}"'

    return textwrap.dedent(f"""<img src="{src}" alt="{alt}"{width}/>""")


@shortcodes.register("rootpage")
@util.timing
def rootpage(pargs, kwargs, node):
    """Handle [% rootpage NAME.md %] shortcode."""
    util.require(
        len(pargs) == 1 and not kwargs,
        f"Bad 'rootpage' shortcode with {pargs} and {kwargs}",
    )
    path = Path(ark.site.home(), pargs[0])
    try:
        return util.FIRST_H1.sub("", path.read_text())
    except OSError:
        util.fail(f"cannot read .ark file {str(path)}")


@shortcodes.register("summary")
@util.timing
def summary(pargs, kwargs, node):
    """Handle [% summary %] shortcode."""
    util.require(
        (not pargs) and ("kind" in kwargs),
        f"Bad 'summary' shortcode in {node} with {pargs} and {kwargs}",
    )
    kind = kwargs["kind"]
    util.require(
        kind in {"abstracts", "summary", "syllabus"},
        f"Unknown kind '{kind}' in summary shortcode"
    )
    with_links = kwargs.get("links", "") != "False"
    with_slides = kwargs.get("slides", "") != "False"

    lines = []
    for slug in ark.site.config["chapters"]:
        meta = ark.site.config["_meta_"][slug]
        util.require("tag" in meta, f"No tag found for {slug}")
        util.require("abstract" in meta, f"No abstract found for {slug}")
        util.require("syllabus" in meta, f"No syllabus data found for {slug}")

        title = f"[{meta['title']}](@root/{slug})" if with_links else meta["title"]
        slides = f"([slides](@root/{slug}/slides.html))" if with_slides else ""
        label = f"{{: #summary-{slug}}}"
        lines.append(f"\n## {title} {slides} {label}\n")
        if kind == "abstracts":
            lines.append(meta["abstract"])
        elif kind == "syllabus":
            for item in meta["syllabus"]:
                lines.append(f"- {item}")

    return "\n".join(lines)


@shortcodes.register("t")
@util.timing
def table_ref(pargs, kwargs, node):
    """Handle [%t slug %] table reference shortcodes."""
    util.require((len(pargs) == 1) and (not kwargs), f"Bad 't' shortcode in {node}")
    slug = pargs[0]
    known = ark.site.config["_tables_"]
    util.require(slug in known, f"Unknown table slug {slug} in {node}")
    return f'<a class="tbl-ref" href="#{slug}">Table&nbsp;{known[slug]}</a>'


@shortcodes.register("table")
@util.timing
def table_def(pargs, kwargs, node):
    """Handle table definition."""
    allowed = {"slug", "tbl", "caption"}
    util.require(
        (not pargs) and allowed.issuperset(kwargs.keys()),
        f"Bad 'table' shortcode {pargs} and {kwargs} in {node}",
    )

    slug = kwargs["slug"]
    tbl = kwargs["tbl"]
    known = ark.site.config["_tables_"]
    label = f"Table&nbsp;{known[slug]}"
    caption = util.markdownify(kwargs["caption"])
    header = (
        f'<table id="{slug}" data-tbl="{tbl}">\n<caption>{label}: {caption}</caption>'
    )

    util.require_file(node, tbl, "table")
    content = util.read_file(node, tbl, "table").strip()
    content = util.markdownify(content, strip_p=False)
    content = content.replace("<table>", header)
    return content


@shortcodes.register("thanks")
@util.timing
def thanks(pargs, kwargs, node):
    """Handle [% thanks %] table of thanks shortcode."""
    util.require(
        (not pargs) and (list(kwargs.keys()) == ["width"]),
        f"Badly-formatted 'thanks' shortcode with {pargs} and {kwargs}",
    )

    filepath = Path(ark.site.home(), "info", "thanks.yml")
    thanks = yaml.safe_load(filepath.read_text()) or []
    thanks = [
        f'<a href="{entry["url"]}">{entry["name"]}</a>'
        if "url" in entry
        else entry["name"]
        for entry in thanks
    ]
    width = int(kwargs["width"])
    columns = _split_list(thanks, width)
    columns = "".join(["<td>" + "<br>".join(c) + "</td>" for c in columns])
    return f'<table class="no-id"><tbody><tr>{columns}</tr></tbody></table>'


@shortcodes.register("toc")
@util.timing
def toc(pargs, kwargs, node):
    """Handle [% toc %] table of contents shortcode."""
    util.require(
        (not pargs),
        f"Bad 'toc' shortcode with {pargs} and {kwargs}",
    )
    with_slides = kwargs.get("slides", "") != "False"

    def _format(slug, is_chapter):
        meta = ark.site.config["_meta_"][slug]
        title = f'<a href="@root/{slug}">{util.markdownify(meta["title"])}</a>'
        tag = f": {util.markdownify(meta['tag'])}" if is_chapter else ""
        show_slides = is_chapter and with_slides
        slides = (
            f' (<a href="@root/{slug}/slides.html">slides</a>)' if show_slides else ""
        )
        return f"<li>{title}{tag}{slides}</li>"

    chapters = [_format(slug, True) for slug in ark.site.config["chapters"]]
    chapters = '<ol class="toc" type="1">\n' + "\n".join(chapters) + "\n</ol>"
    appendices = [_format(slug, False) for slug in ark.site.config["appendices"]]
    appendices = '<ol class="toc" type="A">\n' + "\n".join(appendices) + "\n</ol>"
    return f"{chapters}\n{appendices}"


@shortcodes.register("x")
@util.timing
def x_reference(pargs, kwargs, node):
    """Handle [%x slug %] cross-reference shortcode."""
    util.require(
        (len(pargs) == 1) and (not kwargs),
        f"Bad 'x' shortcode with {pargs} and {kwargs}",
    )
    slug = pargs[0]
    if ark.site.config.get("draft", False) and (
        slug not in ark.site.config["contents"]
    ):
        return '<span class="fixme">see&nbsp;FIXME</span>'
    util.require(
        slug in ark.site.config["_number_"], f"Unknown key in 'x' shortcode {slug}"
    )
    kind = ark.site.config["_number_"][slug]["kind"]
    number = ark.site.config["_number_"][slug]["number"]
    return f"{kind}&nbsp;{number}"


def _split_list(values, width):
    """Split list into (nearly) equal-sized portions."""
    least = len(values) // width
    rem = len(values) % width
    heights = [least + 1 if i < rem else least for i in range(width)]

    base = 0
    result = []
    for h in heights:
        result.append(values[base : base + h])
        base += h
    return result
