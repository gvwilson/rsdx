#!/usr/bin/env python

"""Generate random plates."""

import argparse
import csv
from datetime import datetime, timedelta
import random
import sys

import pytz

MODEL = "Weyland-Yutani 470"
PLATE_HEIGHT = 4
PLATE_WIDTH = 4
TIME_FORMAT = "%Y-%m-%d:%H:%M:%S"


def main():
    """Main driver."""
    args = parse_args()
    random.seed(args.seed)
    for i in range(args.num):
        head = generate_head(args, i)
        placement, sample_locations = generate_placement()
        body = generate_body(args, placement, i)
        foot = generate_foot(sample_locations)
        result = normalize_csv([*head, *body, *foot])
        save(args, result, i)


def generate_body(args, placement, i):
    """Make body of plate."""
    title_row = ["", *[chr(ord("A") + col) for col in range(PLATE_WIDTH)]]
    readings = [
        [f"{reading(args, placement[row][col], i):.02f}" for col in range(PLATE_WIDTH)]
        for row in range(PLATE_HEIGHT)
    ]
    readings = [[str(i + 1), *r] for (i, r) in enumerate(readings)]
    return [title_row, *readings]


def generate_foot(sample_locations):
    """Generate foot of plate."""
    return [[], ["Samples", *sample_locations]]


def generate_head(args, i):
    """Make head of plate."""
    time = datetime.strftime(args.exptime + timedelta(minutes=i), TIME_FORMAT)
    return [
        [MODEL],
        ["Recorded", time],
        [],
    ]


def generate_placement():
    """Generate random placement of samples."""
    placement = [[False for col in range(PLATE_WIDTH)] for row in range(PLATE_HEIGHT)]
    columns = list(c for c in range(PLATE_WIDTH))
    random.shuffle(columns)
    columns = columns[:PLATE_HEIGHT]
    for (r, row) in enumerate(placement):
        row[columns[r]] = True
    return placement, columns


def normalize_csv(rows):
    required = max(len(r) for r in rows)
    for row in rows:
        row.extend([""] * (required - len(row)))
    return rows


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--control", type=float, required=True, help="expected value for untreated wells"
    )
    parser.add_argument("--exptime", type=str, default=None, help="reading date/time")
    parser.add_argument("--num", type=int, required=True, help="number of plates")
    parser.add_argument("--seed", type=int, required=True, help="RNG seed")
    parser.add_argument("--stem", type=str, help="output file stem")
    parser.add_argument("--stdev", type=float, required=True, help="sample standard deviation")
    parser.add_argument(
        "--treated", type=float, required=True, help="expected value for treated wells"
    )
    args = parser.parse_args()
    args.exptime = datetime.strptime(args.exptime, TIME_FORMAT)
    return args


def reading(args, treated, iteration):
    """Generate a single plate reading."""
    mean = args.treated if treated else args.control
    mean += 0.01 * iteration * mean  # temporal effect
    return max(0.0, random.gauss(mean, args.stdev))


def save(args, rows, i):
    """Save as CSV."""
    if not args.stem:
        csv.writer(sys.stdout).writerows(rows)
    else:
        filename = f"{args.stem}-{i:02}.csv"
        with open(filename, "w") as writer:
            csv.writer(writer).writerows(rows)


if __name__ == "__main__":
    main()
