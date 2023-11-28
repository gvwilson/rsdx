"""Ark shortcodes."""

import csv
from pathlib import Path

from prettytable import PrettyTable
import shortcodes


@shortcodes.register("csv")
def display_csv(pargs, kwargs, node):
    """Handle [%csv filename %] table inclusion."""
    assert (len(pargs) == 1) and (
        not kwargs
    ), f"Bad 'csv' shortcode with {pargs} and {kwargs} in {node}"
    filepath = Path(pargs[0])
    assert filepath.exists(), f"CSV file {filepath} not found"
    with open(filepath, "r") as raw:
        rows = [[val if val else "…" for val in row] for row in csv.reader(raw)]
    tbl = PrettyTable(header=False)
    tbl.add_rows(rows)
    return tbl.get_html_string()


@shortcodes.register("root")
def include_root_file(pargs, kwargs, node):
    """Handle [%root filename %] file inclusion."""
    assert (len(pargs) == 1) and (
        not kwargs
    ), f"Bad 'csv' shortcode with {pargs} and {kwargs} in {node}"
    filepath = Path(pargs[0])
    assert filepath.exists(), f"CSV file {filepath} not found"
    text = filepath.read_text()
    if text.startswith("# "):
        text = text.split("\n", 1)[1]
    return text
