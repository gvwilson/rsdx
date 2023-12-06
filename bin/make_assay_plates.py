#!/usr/bin/env python

"""Generate random plates."""

import argparse
import csv
import random
import sys

import pytz

MODEL = "Weyland-Yutani 470"
PLATE_HEIGHT = 4
PLATE_WIDTH = 4


def main():
    """Main driver."""
    args = parse_args()
    random.seed(args.seed)
    generate_plate(args, args.outfile)


def generate_plate(args, outfile):
    """Generate an entire plate."""
    head = _gen_head(args)
    placement, sample_locs = _gen_placement()
    body = _gen_body(args, placement)
    foot = _gen_foot(sample_locs)
    plate = _normalize_csv([*head, *body, *foot])
    _save(outfile, plate)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--control", type=float, required=True, help="expected value for untreated wells"
    )
    parser.add_argument("--outfile", type=str, help="output file")
    parser.add_argument("--seed", type=int, required=True, help="RNG seed")
    parser.add_argument("--stdev", type=float, required=True, help="sample standard deviation")
    parser.add_argument(
        "--treated", type=float, required=True, help="expected value for treated wells"
    )
    return parser.parse_args()


def _gen_body(args, placement):
    """Make body of plate."""
    title_row = ["", *[chr(ord("A") + col) for col in range(PLATE_WIDTH)]]
    readings = [
        [f"{_reading(args, placement[row][col]):.02f}" for col in range(PLATE_WIDTH)]
        for row in range(PLATE_HEIGHT)
    ]
    readings = [[str(i + 1), *r] for (i, r) in enumerate(readings)]
    return [title_row, *readings]


def _gen_foot(sample_locs):
    """Generate foot of plate."""
    return [[], ["Samples", *sample_locs]]


def _gen_head(args):
    """Make head of plate."""
    return [
        [MODEL],
        [],
    ]


def _gen_placement():
    """Generate random placement of samples."""
    placement = [[False for col in range(PLATE_WIDTH)] for row in range(PLATE_HEIGHT)]
    columns = list(c for c in range(PLATE_WIDTH))
    random.shuffle(columns)
    columns = columns[:PLATE_HEIGHT]
    for (r, row) in enumerate(placement):
        row[columns[r]] = True
    return placement, columns


def _normalize_csv(rows):
    required = max(len(r) for r in rows)
    for row in rows:
        row.extend([""] * (required - len(row)))
    return rows


def _reading(args, treated):
    """Generate a single plate reading."""
    mean = args.treated if treated else args.control
    return max(0.0, random.gauss(mean, args.stdev))


def _save(filename, rows):
    """Save as CSV."""
    if not filename:
        csv.writer(sys.stdout).writerows(rows)
    else:
        with open(filename, "w") as writer:
            csv.writer(writer).writerows(rows)


if __name__ == "__main__":
    main()
