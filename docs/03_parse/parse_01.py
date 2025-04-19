import argparse
import csv
from datetime import date


HEADER = (
    ("id", int),
    ("specimen", str),
    ("date", date.fromisoformat),
    ("by", str),
    ("machine", str),
)


def cmdline_args():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--files", nargs="+", required=True, help="filenames")
    return parser.parse_args()


def parse_assay(filename):
    """Parse specified assay file."""

    with open(filename, "r") as reader:
        rows = [r for r in csv.reader(reader)]
    result = {}
    for i, (key, converter) in enumerate(HEADER):
        if rows[i][0] != key:
            raise ValueError(f"row {i} of {filename}: expected {key} got {rows[i][0]}")
        result[key] = converter(rows[i][1])
    return result


if __name__ == "__main__":
    args = cmdline_args()
    for filename in args.files:
        assay = parse_assay(filename)
        print(assay)
