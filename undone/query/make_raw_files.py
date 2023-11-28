"""Make plate files."""

import argparse
import csv
from pathlib import Path
import random
import sqlite3

from rsdx import make_plate

CALIBRATION_EMPTY = 0.25
QUERY = """\
select kind, filename
from experiment inner join plate
on experiment.ident = plate.experiment;
"""


def main():
    """Main driver."""
    args = parse_args()
    random.seed(args.seed)
    connection = sqlite3.connect(args.dbfile)
    cursor = connection.execute(QUERY)
    for kind, filename in cursor:
        frac = CALIBRATION_EMPTY if kind == "calibration" else 0.0
        plate = make_plate(None, frac)
        with open(Path(args.outdir, filename), "w") as writer:
            csv.writer(writer).writerows(plate)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbfile", type=str, required=True, help="database file")
    parser.add_argument("--outdir", type=str, required=True, help="output directory")
    parser.add_argument("--seed", type=int, required=True, help="RNG seed")
    return parser.parse_args()


if __name__ == "__main__":
    main()
