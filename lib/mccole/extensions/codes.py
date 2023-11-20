"""Ark shortcodes."""

from pathlib import Path

import ark
import pybtex.plugin
import shortcodes
import yaml

import regex
import util


@shortcodes.register("b")
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
def bibliography(pargs, kwargs, node):
    """Handle [% bibliography %] shortcode."""

    def _fmt(key, body):
        return f'<dt id="{key}" class="bib-def">{key}</dt>\n<dd>{body}</dd>'

    util.require(
        (not pargs) and (not kwargs),
        f"Bad 'bibliography' shortcode with {pargs} and {kwargs} in {node}",
    )

    styled_bib = ark.site.config["_bib_"]
    html = pybtex.plugin.find_plugin("pybtex.backends", "html")()
    entries = [_fmt(entry.key, entry.text.render(html)) for entry in styled_bib]
    return '<dl class="bib-list">\n\n' + "\n\n".join(entries) + "\n\n</dl>"


@shortcodes.register("date")
def date(pargs, kwargs, node):
    """Handle [% date %] shortcode."""
    util.require(
        (not pargs) and (not kwargs),
        f"Bad 'date' shortcode with {pargs} and {kwargs}",
    )
    return ark.site.config["_date_"]


@shortcodes.register("f")
def figure_ref(pargs, kwargs, node):
    """Handle [%f slug %] figure reference shortcodes."""
    util.require((len(pargs) == 1) and (not kwargs), f"Bad 'f' shortcode in {node}")
    slug = pargs[0]
    known = ark.site.config["_figures_"]
    util.require(slug in known, f"Unknown figure slug {slug} in {node}")
    return f'<a class="fig-ref" href="#{slug}">Figure&nbsp;{known[slug]}</a>'


@shortcodes.register("figure")
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
    alt = util.markdownify(kwargs["alt"], True)
    caption = util.markdownify(kwargs["caption"], True)

    util.require_file(node, img, "figure")
    known = ark.site.config["_figures_"]

    label = f"Figure&nbsp;{known[slug]}"
    body = f'<img src="./{img}" alt="{alt}"{scale}/>'
    caption = f'<figcaption markdown="1">{label}: {caption}</figcaption>'
    return f'<figure id="{slug}"{cls}>\n{body}\n{caption}\n</figure>'


@shortcodes.register("fixme")
def fixme(pargs, kwargs, node):
    """Handle [% fixme 'item' ... %] shortcode."""
    util.require(
        (len(pargs) > 0) and (not kwargs),
        f"Bad 'fixme' shortcode with {pargs} and {kwargs}",
    )
    if len(pargs) == 1:
        return f'<span class="fixme" markdown="1">{pargs[0]}</span>'
    items = "\n".join(f"-   {x}" for x in pargs)
    return f'<div class="fixme" markdown="1">\n{items}\n</div>'


@shortcodes.register("rootpage")
def rootpage(pargs, kwargs, node):
    """Handle [% rootpage NAME.md %] shortcode."""
    util.require(
        len(pargs) == 1 and not kwargs,
        f"Bad 'rootpage' shortcode with {pargs} and {kwargs}",
    )
    path = Path(ark.site.home(), pargs[0])
    try:
        return regex.FIRST_H1.sub("", path.read_text())
    except OSError:
        util.fail(f"cannot read .ark file {str(path)}")


@shortcodes.register("syllabus")
def syllabus(pargs, kwargs, node):
    """Handle [% syllabus %] shortcode."""
    util.require((not pargs) and (not kwargs), f"Bad 'syllabus' shortcode in {node}")
    meta = ark.site.config["_meta_"]
    lines = []
    for slug in ark.site.config["chapters"]:
        if "syllabus" not in meta[slug]:
            continue
        lines.append(
            f"\n## [{meta[slug]['title']}](@root/{slug}) {{: #syllabus-{slug}}}\n"
        )
        for item in meta[slug]["syllabus"]:
            lines.append(f"- {item}")
    return "\n".join(lines)


@shortcodes.register("t")
def table_ref(pargs, kwargs, node):
    """Handle [%t slug %] table reference shortcodes."""
    util.require((len(pargs) == 1) and (not kwargs), f"Bad 't' shortcode in {node}")
    slug = pargs[0]
    known = ark.site.config["_tables_"]
    util.require(slug in known, f"Unknown table slug {slug} in {node}")
    return f'<a class="tbl-ref" href="#{slug}">Table&nbsp;{known[slug]}</a>'


@shortcodes.register("table")
def table_def(pargs, kwargs, node):
    """Handle table definition."""
    allowed = {"slug", "tbl", "caption"}
    util.require(
        (not pargs) and allowed.issuperset(kwargs.keys()),
        f"Bad 'table' shortcode {pargs} and {kwargs} in {node}",
    )

    slug = kwargs["slug"]
    tbl = kwargs["tbl"]
    caption = util.markdownify(kwargs["caption"], True)
    header = f'<table id="{slug}" data-tbl="{tbl}">\n<caption>{caption}</caption>'

    util.require_file(node, tbl, "table")
    content = util.markdownify(util.read_file(node, tbl, "table").strip())
    content = content.replace("<table>", header)
    return content


@shortcodes.register("thanks")
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
    return f'<table class="no-id"><tr>{columns}</tr></table>'


@shortcodes.register("toc")
def toc(pargs, kwargs, node):
    """Handle [% toc %] table of contents shortcode."""
    util.require(
        (not pargs) and (not kwargs), f"Bad 'toc' shortcode with {pargs} and {kwargs}"
    )
    chapters = []
    appendices = []
    for slug in ark.site.config["chapters"]:
        title = ark.site.config["_meta_"][slug]["title"]
        entry = f'<li><a href="@root/{slug}/">{title}</a></li>'
        if "tag" in ark.site.config["_meta_"][slug]:
            chapters.append(entry)
        else:
            appendices.append(entry)
    chapters = '<ol class="toc" type="1">\n' + "\n".join(chapters) + "\n</ol>"
    appendices = '<ol class="toc" type="A">\n' + "\n".join(appendices) + "\n</ol>"
    return f"{chapters}\n{appendices}"


@shortcodes.register("x")
def x_reference(pargs, kwargs, node):
    """Handle [%x slug %] cross-reference shortcode."""
    util.require(
        (len(pargs) == 1) and (not kwargs),
        f"Bad 'x' shortcode with {pargs} and {kwargs}",
    )
    slug = pargs[0]
    if ark.site.config.get("draft", False) and (
        slug not in ark.site.config["chapters"]
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
        result.append(values[base:base+h])
        base += h
    return result
