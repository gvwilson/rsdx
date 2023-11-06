"""Ark shortcodes."""

from pathlib import Path
import re

import ark
import shortcodes

import util


FIRST_H1 = re.compile(r"^#\s+.+$", re.MULTILINE)


@shortcodes.register("date")
def date(pargs, kwargs, node):
    """Handle [% date %] shortcode."""
    util.require(
        (not pargs) and (not kwargs),
        f"Bad 'date' shortcode with {pargs} and {kwargs}",
    )
    return util.get_date()


@shortcodes.register("rootpage")
def rootpage(pargs, kwargs, node):
    """Handle [% rootpage NAME.md %] shortcode."""
    util.require(
        len(pargs) == 1 and not kwargs,
        f"Bad 'rootpage' shortcode with {pargs} and {kwargs}",
    )
    path = Path(ark.site.home(), pargs[0])
    try:
        with open(path, "r") as reader:
            return FIRST_H1.sub("", reader.read())
    except OSError:
        util.fail(f"cannot read .ark file {str(path)}")


@shortcodes.register("toc")
def toc(pargs, kwargs, node):
    """Handle [% toc %] table of contents shortcode."""
    util.require(
        (not pargs) and (not kwargs), f"Bad 'toc' shortcode with {pargs} and {kwargs}"
    )
    items = "\n".join(
        [
            f'<li><a href="@root/{slug}/">{title}</a></li>'
            for slug, title in ark.site.config["chapters"].items()
        ]
    )
    return f'<ol class="toc">\n{items}\n</ol>'
