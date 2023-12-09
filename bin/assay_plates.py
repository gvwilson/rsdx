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
    create_plate_files(args, params, connection)


def create_plate_files(args, params, connection):
    """Create randomized plate files."""
    cursor = connection.execute(PLATE_QUERY)
    rows = cursor.fetchall()
    for kind, filename in rows:
        generate_plate(params, Path(args.platedir, filename), kind)


def generate_plate(params, outfile, kind):
    """Generate an entire plate."""
    head = _gen_head(params)
    placement, sample_locs = _gen_placement(kind)
    body = _gen_body(params, placement)
    foot = _gen_foot(sample_locs)
    plate = _normalize_csv([*head, *body, *foot])
    _save(outfile, plate)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbfile", type=str, required=True, help="database file")
    parser.add_argument("--params", type=str, required=True, help="parameter file")
    parser.add_argument("--platedir", type=str, required=True, help="plate directory")
    return parser.parse_args()


def _gen_body(params, placement):
    """Make body of plate."""
    title_row = ["", *[chr(ord("A") + col) for col in range(PLATE_WIDTH)]]
    readings = [
        [_reading(params, placement[row][col]) for col in range(PLATE_WIDTH)]
        for row in range(PLATE_HEIGHT)
    ]
    readings = [[str(i + 1), *r] for (i, r) in enumerate(readings)]
    return [title_row, *readings]


def _gen_foot(sample_locs):
    """Generate foot of plate."""
    return [[], ["Samples", *sample_locs]]


def _gen_head(params):
    """Make head of plate."""
    return [
        [MODEL],
        [],
    ]


def _gen_placement(kind):
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
