import argparse
import csv
from datetime import date
import polars as pl


HEADER_LEN = 5


def cmdline_args():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--files", nargs="+", required=True, help="filenames")
    return parser.parse_args()


def parse_assay(filename, people):
    """Parse specified assay file."""

    with open(filename, "r") as reader:
        rows = [r for r in csv.reader(reader)]
    consumed, result = _parse_header(rows, people)
    result["data"] = _parse_body(rows)
    return result


def _convert_id(value, extra=None):
    """Convert assay ID that might be quoted."""

    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    return int(value)


def _convert_specimen(value, extra=None):
    """Convert specimen ID."""

    return value


def _convert_date(value, extra=None):
    """Convert ISO formatted date."""

    return date.fromisoformat(value)


def _convert_by(value, extra):
    """Convert person ID or name."""

    return value


def _convert_machine(value, extra=None):
    """Convert machine ID."""

    return value


def _parse_body(rows):
    """Parse the body."""

    schema = rows[HEADER_LEN]
    schema[0] = "row"
    df = pl.DataFrame(rows[HEADER_LEN + 1 :], orient="row", schema=schema)
    return df.with_columns(
        pl.col("row").cast(pl.Int64), pl.col("*").exclude("row").cast(pl.Float64)
    )


def _parse_header(rows, people):
    """Parse the header."""

    converters = (
        ("id", _convert_id),
        ("specimen", _convert_specimen),
        ("date", _convert_date),
        ("by", _convert_by),
        ("machine", _convert_machine),
    )
    assert len(converters) == HEADER_LEN, (
        "mis-match in converter table and header length"
    )

    result = {}
    i = 0
    for key, converter in converters:
        if rows[i][0] != key:
            result[key] = None
        else:
            result[key] = converter(rows[i][1], people)
            i += 1

    return i, result


if __name__ == "__main__":
    args = cmdline_args()
    people = {"Kristi Nõmmik": "nk3892"}
    for filename in args.files:
        assay = parse_assay(filename, people)
        print(assay)
