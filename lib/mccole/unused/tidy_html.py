"""Tidy up HTML after generation by re-parsing, modifying, and re-saving."""

import BeautifulSoup
import ark


@ark.events.register(ark.events.Event.RENDER_PAGE)
def tidy_html(arg):
    doc = BeautifulSoup(arg["node"].html, "html.parser")
    for name, func in globals().items():
        if name.startswith("_tidy_"):
            func(doc)
    arg["node"].cache["html"] = str(doc)


def _tidy_table_divs(doc):
    """Replace div nodes containing tables with proper tables."""
    for div in doc.find_all("div", class_="table"):
        table = div.find("table")
        caption = div.find("caption")
        if table and caption and ("id" in table.attrs):
            table.attrs["id"] = div.attrs["id"]
            div.replace_with(table)
            table.insert(0, caption)
