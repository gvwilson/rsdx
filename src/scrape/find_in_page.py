import argparse
from bs4 import BeautifulSoup
from pathlib import Path


def main():
    """Parse page and visit nodes."""
    options = parse_args()
    text = Path(options.filename).read_text()
    doc = BeautifulSoup(text, "html.parser")
    for node in doc.find_all(options.tag):
        print(f"{node.name} with {node.attrs}")


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str, required=True, help="HTML file")
    parser.add_argument("--tag", type=str, required=True, help="tag to search for")
    return parser.parse_args()


if __name__ == "__main__":
    main()
