"""Ark shortcodes."""

from pathlib import Path
import re

import ark
import shortcodes


FIRST_H1 = re.compile(r"^#\s+.+$", re.MULTILINE)


@shortcodes.register("rootpage")
def rootpage(pargs, kwargs, node):
    """Handle [% rootpage NAME.md %] shortcode."""
    path = Path(ark.site.home(), pargs[0])
    with open(path, "r") as reader:
        return FIRST_H1.sub("", reader.read())


@shortcodes.register("toc")
def toc(pargs, kwargs, node):
    """Handle [% toc %] table of contents shortcode."""
    items = "\n".join([
        f'<li><a href="@root/{slug}/">{title}</a></li>'
        for slug, title in ark.site.config["chapters"].items()
    ])
    return f'<ol class="toc">\n{items}\n</ol>'
