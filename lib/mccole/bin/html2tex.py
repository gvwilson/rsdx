"""Convert HTML pages to LaTeX."""

import argparse
from pathlib import Path
import sys

from bs4 import BeautifulSoup, NavigableString, Tag

import util


LATEX_FIG_SCALE = 0.8


def main():
    """Main driver."""
    args = parse_args()
    config = util.load_config(args.config)
    pages = util.collect_files(config, "html", False)
    doc = extract_contents(pages)
    body = "".join(do(doc, None, [], escape_chars))
    head, foot = get_tex_head_foot(args.config, config)
    if args.outfile:
        save(open(args.outfile, "w"), head, body, foot)
    else:
        save(sys.stdout, head, body, foot)


def children(node, slug, accum, escape, before=None, after=None):
    """Handle children of containing node."""
    if before is not None:
        accum.append(before)

    for child in node:
        do(child, slug, accum, escape)

    if after is not None:
        accum.append(after)

    return accum


def citation(node, slug, accum, escape):
    """Handle a group of citations."""
    cites = node.find_all("a")
    assert all(has_class(child, "bib-ref") for child in cites)
    keys = ",".join([c["href"].split("#")[1] for c in cites])
    accum.append(rf"\cite{{{keys}}}")


def do(node, slug, accum, escape):
    """Dispatch to accumulate conversion for node."""

    # Text content => escape (or not).
    if isinstance(node, NavigableString):
        accum.append(escape(node.string))

    # Not a node => do nothing.
    elif not isinstance(node, Tag):
        pass

    # Root.
    elif match(node, "[document]"):
        children(node, slug, accum, escape)

    # '<a class="fig-ref" href="...">' figure reference.
    elif match(node, "a", "fig-ref"):
        key = href_key(node)
        accum.append(rf"\figref{{{key}}}")

    # '<a class="tbl-ref" href="...">' table reference.
    elif match(node, "a", "tbl-ref"):
        key = href_key(node)
        accum.append(rf"\tblref{{{key}}}")

    # '<a href="...">' with no class.
    elif match(node, "a"):
        children(node, slug, accum, escape)

    # '<blockquote>' quotation.
    elif match(node, "blockquote"):
        children(
            node, slug, accum, escape, "\\begin{quotation}\n", "\\end{quotation}\n"
        )

    # '<br>' line break.
    elif match(node, "br"):
        accum.append("\\\\\n")

    # '<code>' inline code.
    elif match(node, "code"):
        temp = "".join(children(node, slug, [], escape))
        temp = temp.replace("'", r"{\textquotesingle}")
        accum.append(rf"\texttt{{{temp}}}")

    # '<div class="callout">' callout block.
    elif match(node, "div", "callout"):
        children(node, slug, accum, escape, "\\begin{callout}\n", "\\end{callout}\n")

    # '<div class="center">' callout block.
    elif match(node, "div", "center"):
        children(node, slug, accum, escape, "\\begin{center}\n", "\\end{center}\n")

    # '<div class="fixme">' list of problems.
    elif match(node, "div", "fixme"):
        children(node, slug, accum, escape, r"\begin{fixme}", r"\end{fixme}")

    # '<div class="notex">' skip.
    elif match(node, "div", "notex"):
        pass

    # '<div class="title"> insert title.
    elif match(node, "div", {"title"}):
        h1 = node.find("h1")
        title = "".join(children(h1, slug, [], escape))
        accum.extend([r"\chapter{", title, r"}\label{", slug, "}\n"])

    # '<dd>' body of labeled itemize.
    elif match(node, "dd"):
        children(node, slug, accum, escape)
        accum.append("\n\n")

    # '<dl>' description list.
    elif match(node, "dl"):
        children(node, slug, accum, escape)

    # '<dt>' description list key.
    elif match(node, "dt"):
        children(node, slug, accum, escape, r"\noindent \textbf{", "}: ")

    # '<em>' italics.
    elif match(node, "em"):
        children(node, slug, accum, escape, r"\emph{", "}")

    # '<figure>' figure.
    elif match(node, "figure"):
        figure(node, slug, accum, escape)

    # 'h2' section title.
    elif match(node, "h2"):
        title = "".join(children(node, slug, [], escape))
        if node.has_attr("id"):
            accum.extend([r"\section{", title, r"}\label{", node["id"], "}\n"])
        else:
            accum.extend([r"\section*{", title, "}\n"])

    # '<h3>' inside '<div class="callout">' callout title
    elif (
        (node.name == "h3")
        and (node.parent.name == "div")
        and has_class(node.parent, "callout")
    ):
        children(node, slug, accum, escape, "\n\\subsubsection*{", "}\n")

    # other '<h3>' subsection
    elif match(node, "h3"):
        children(node, slug, accum, escape, r"\subsection*{", "}\n")

    # '<li>' list item.
    elif match(node, "li"):
        children(node, slug, accum, escape, r"\item ", "\n")

    # '<main>' whole chapter.
    elif match(node, "main"):
        slug = node.attrs.get("data-slug", None)
        children(node, slug, accum, escape)

    # '<ol>' ordered list.
    elif match(node, "ol"):
        children(
            node, slug, accum, escape, "\\begin{enumerate}\n", "\\end{enumerate}\n"
        )

    # '<p class="continue"> unindented continuation paragraph.
    elif match(node, "p", "continue"):
        children(node, slug, accum, escape, "\n\\noindent ", "\n")

    # '<p>' => paragraph.
    elif match(node, "p"):
        children(node, slug, accum, escape, "\n")

    # '<span class="bib-ref">' citations.
    elif match(node, "span", "bib-ref"):
        citation(node, slug, accum, escape)

    # '<span class="bibtex-protected">' inserted by other tool.
    elif match(node, "span", "bibtex-protected"):
        citation(node, slug, accum, escape)

    # '<span class="fixme">' markers.
    elif match(node, "span", "fixme"):
        children(node, slug, accum, escape, r"\textbf{FIXME: ", "}")

    # '<strong>' bold text.
    elif match(node, "strong"):
        children(node, slug, accum, escape, r"\textbf{", "}")

    # '<table>' table.
    elif match(node, "table"):
        table(node, slug, accum, escape)

    # '<td>' table cell.
    elif match(node, "td"):
        children(node, slug, accum, escape)

    # '<th>' table header cell.
    elif match(node, "th"):
        children(node, slug, accum, escape)

    # '<ul>' unordered list.
    elif match(node, "ul"):
        children(node, slug, accum, escape, "\\begin{itemize}\n", "\\end{itemize}\n")

    # Unhandled.
    else:
        util.fail(f"Unknown node type {type(node)} / {node.name}: '{node}'")

    # Report back.
    return accum


def escape_chars(text):
    """Escape special characters."""
    return (
        text.replace("{", "ACTUAL-LEFT-CURLY-BRACE")
        .replace("}", "ACTUAL-RIGHT-CURLY-BRACE")
        .replace("\\", r"{\textbackslash}")
        .replace("$", r"\$")
        .replace("%", r"\%")
        .replace("_", r"\_")
        .replace("^", r"{\textasciicircum}")
        .replace("#", r"\#")
        .replace("&", r"\&")
        .replace("<<<", r"<\null<\null<")
        .replace(">>>", r">\null>\null>")
        .replace("<<", r"<\null<")
        .replace(">>", r">\null>")
        .replace("~", r"$\sim$")
        .replace("©", r"{\textcopyright}")
        .replace("μ", r"{\textmu}")
        .replace("…", "...")
        .replace("ACTUAL-LEFT-CURLY-BRACE", r"\{")
        .replace("ACTUAL-RIGHT-CURLY-BRACE", r"\}")
    )


def escape_noop(text):
    """Pretend to escape (needed to simplify calling)."""
    return text


def extract_contents(pages):
    """Extract all content sections from pages."""
    doc = BeautifulSoup()
    for p in pages.values():
        doc.append(p.find("main"))
    return doc


def figure(node, slug, accum, escape):
    """Handle figure."""
    assert node.name == "figure", "Not a figure"
    label = node["id"]
    command = (
        "figpdfhere"
        if (node.has_attr("class") and "here" in node["class"])
        else "figpdf"
    )
    scale = (
        float(node.img["width"].rstrip("%")) / 100
        if node.img.has_attr("width")
        else LATEX_FIG_SCALE
    )
    path = Path(slug, node.img["src"].replace(".svg", ".pdf"))
    caption = "".join(children(node.figcaption, slug, [], escape))
    caption = caption.split(":", 1)[1].strip()
    accum.append(f"\\{command}{{{label}}}{{{path}}}{{{caption}}}{{{scale}}}\n")


def get_tex_head_foot(config_path, config):
    """Get extra LaTeX."""
    root_dir = Path(config_path).parent
    head = Path(root_dir, "lib", config.theme, "info", "head.tex").read_text()
    foot = Path(root_dir, "lib", config.theme, "info", "foot.tex").read_text()

    attrib = f"\\title{{{config.title}}}\n\\author{{{config.author}}}\n"
    head = head.replace("% AUTHOR_TITLE", attrib)

    return head, foot


def has_class(node, class_):
    """Check if node has one of the specified classes."""
    if not node.has_attr("class"):
        return False
    if isinstance(class_, str):
        return class_ in node["class"]
    return any(c in node["class"] for c in class_)


def href_key(node):
    """Get key from href attribute if available."""
    if "#" in node["href"]:
        return node["href"].split("#")[1]
    return node["href"]


def match(node, name, class_=None):
    """Does this node match requirements?"""
    if node.name != name:
        return False
    if class_ is None:
        return True
    return has_class(node, class_)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True, help="config file")
    parser.add_argument("--outfile", type=str, default=None, help="output file")
    return parser.parse_args()


def save(writer, *items):
    """Save results."""
    for i in items:
        writer.write(i)


def table(node, slug, accum, escape):
    """Convert a table."""
    assert node.name == "table", "Node is not a table"
    label = node["id"] if node.has_attr("id") else None
    class_pos = node["class"] if node.has_attr("class") else []
    latex_pos = "[h]" if ("here" in class_pos) else ""

    assert node.tbody, f"Table node does not have body {node}"
    rows = [table_row(row, slug, escape, "td") for row in node.tbody.find_all("tr")]
    width = len(node.tbody.find("tr").find_all("td"))
    spec = r"p{0.48\textwidth}" * 2 if has_class(node, "twocol") else "l" * width

    if node.thead:
        rows = [table_head(node.thead, slug, escape), *rows]

    if label:
        caption = "".join(children(node.caption, slug, [], escape))
        caption = caption.split(":")[1].strip()
        accum.append(f"\\begin{{table}}{latex_pos}\n")
    else:
        accum.append("\n\\vspace{\\baselineskip}\n")

    accum.append(f"\\begin{{tabular}}{{{spec}}}\n")
    accum.append("\n".join(rows))
    accum.append("\n\\end{tabular}\n")
    if label:
        accum.append(f"\\caption{{{caption}}}\n")
        accum.append(f"\\label{{{label}}}\n")
        accum.append("\\end{table}\n")
    else:
        accum.append("\n\\vspace{\\baselineskip}\n")


def table_head(thead, slug, escape):
    """Create head of table."""
    row = thead.tr
    assert row, f"Table head does not have row {thead}"
    headers = row.find_all("th")
    assert headers, f"Table node does not have headers {thead}"
    return table_row(row, slug, escape, "th")


def table_row(row, slug, escape, tag):
    """Convert a single row of a table to a string."""
    cells = row.find_all(tag)
    result = []
    for cell in cells:
        temp = do(cell, slug, [], escape)
        temp = "".join(temp)
        if tag == "th":
            temp = rf"\textbf{{\underline{{{temp}}}}}"
        result.append(temp)
    return " & ".join(result) + r" \\"


if __name__ == "__main__":
    main()
