#!/usr/bin/env python

"""Generate random plates."""

import argparse
import csv
from pathlib import Path
import random
import sqlite3
import sys

from assay_params import load_params


MODEL = "Weyland-Yutani 470"
PLATE_HEIGHT = 4
PLATE_WIDTH = 4
PLATE_QUERY = """\
select experiment.kind, plate.filename
from experiment inner join plate
on experiment.ident = plate.experiment
"""


def main():
    """Main driver."""
    args = parse_args()
    params = load_params(args.params)
    random.seed(params.seed)
    connection = sqlite3.connect(args.dbfile)
    create_files(args, params, connection)


def create_files(args, params, connection):
    """Create randomized plate files."""
    cursor = connection.execute(PLATE_QUERY)
    rows = cursor.fetchall()
    for kind, filename in rows:
        create_one(
            params,
            kind,
            design_file=Path(args.designs, filename),
            results_file=Path(args.results, filename),
        )


def create_one(params, kind, design_file, results_file):
    """Generate an entire plate."""
    placement, sample_locs = _placement(kind)
    head = _head(params)

    design = [*head, *generate(params, placement, _content)]
    _save(design_file, _normalize_csv(design))

    results = [*head, *generate(params, placement, _reading)]
    _save(results_file, _normalize_csv(results))


def generate(params, placement, func):
    """Make body of plate design or results."""
    title_row = ["", *[chr(ord("A") + col) for col in range(PLATE_WIDTH)]]
    values = [
        [func(params, placement[row][col]) for col in range(PLATE_WIDTH)]
        for row in range(PLATE_HEIGHT)
    ]
    labeled = [[str(i + 1), *r] for (i, r) in enumerate(values)]
    return [title_row, *labeled]


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbfile", type=str, required=True, help="database file")
    parser.add_argument("--designs", type=str, required=True, help="designs directory")
    parser.add_argument("--params", type=str, required=True, help="parameter file")
    parser.add_argument("--results", type=str, required=True, help="results directory")
    return parser.parse_args()


def _content(params, treated):
    """Generate a single plate treatment."""
    return params.treatment if treated else random.choice(params.controls)


def _head(params):
    """Make head of plate."""
    return [
        [MODEL],
        [],
    ]


def _placement(kind):
    """Generate random placement of samples."""
    placement = [[False for col in range(PLATE_WIDTH)] for row in range(PLATE_HEIGHT)]
    if kind == "calibration":
        return placement, []
    columns = list(c for c in range(PLATE_WIDTH))
    random.shuffle(columns)
    columns = columns[:PLATE_HEIGHT]
    for r, row in enumerate(placement):
        row[columns[r]] = True
    return placement, columns


def _normalize_csv(rows):
    required = max(len(r) for r in rows)
    for row in rows:
        row.extend([""] * (required - len(row)))
    return rows


def _reading(params, treated):
    """Generate a single plate reading."""
    mean = params.treated if treated else params.control
    value = max(0.0, random.gauss(mean, params.stdev))
    return f"{value:.02f}"


def _save(filename, rows):
    """Save as CSV."""
    if not filename:
        csv.writer(sys.stdout).writerows(rows)
    else:
        with open(filename, "w") as writer:
            csv.writer(writer, lineterminator="\n").writerows(rows)


if __name__ == "__main__":
    main()
