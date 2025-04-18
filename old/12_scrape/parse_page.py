import argparse
from bs4 import BeautifulSoup, NavigableString, Tag
from pathlib import Path


# [main]
def main():
    """Parse page and visit nodes."""
    options = parse_args()
    text = Path(options.filename).read_text()
    doc = BeautifulSoup(text, "html.parser")
    visit(doc, options.noblanks)
# [/main]


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--noblanks", action="store_true", default=False, help="hide empty strings")
    parser.add_argument("--filename", type=str, required=True, help="HTML file")
    return parser.parse_args()


# [visit]
def visit(node, noblanks, depth=0):
    """Show nodes in DOM tree."""
    prefix = "  " * depth
    if isinstance(node, NavigableString):
        if (not noblanks) or node.string.strip():
            print(f"{prefix}text: {repr(node.string)}")
    elif isinstance(node, Tag):
        print(f"{prefix}element: {node.name} with {node.attrs}")
        for child in node:
            visit(child, noblanks, depth+1)
# [/visit]


if __name__ == "__main__":
    main()
