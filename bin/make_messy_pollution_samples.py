"""Work backward from clean CSV to messy CSV for parsing."""

import argparse
import csv
import pandas as pd
from pathlib import Path


COLUMNS = ["site", "date", "lon", "lat", "reading"]
ANALYSTS = [None, "P. Srinath", None]
HEADER_BLANKS = [0, 1, 0, 2]
BODY_INSET = [0, 0, 1]
CAPITALIZE = [False, True, False]


def main():
    """Main driver."""
    args = parse_args()
    for i, tidy_file in enumerate(Path(args.tidydir).glob("*.csv")):
        site = tidy_file.stem
        df = pd.read_csv(tidy_file)
        records = make_records(
            df,
            site,
            ANALYSTS[i % len(ANALYSTS)],
            HEADER_BLANKS[i % len(HEADER_BLANKS)],
            BODY_INSET[i % len(BODY_INSET)],
            CAPITALIZE[i % len(CAPITALIZE)],
        )
        outfile = Path(args.rawdir, f"{site}.csv")
        with open(outfile, "w") as writer:
            csv.writer(writer, lineterminator="\n").writerows(records)


def make_records(df, site, analyst, header_blanks, body_inset, capitalize):
    """Create mangled records as list-of-lists."""
    records = [[row[col] for col in COLUMNS] for row in df.to_dict(orient="records")]

    titles = [s.upper() if capitalize else s for s in COLUMNS]
    records = [titles, *records]

    inset = [""] * body_inset
    records = [inset + row for row in records]

    header = [["Site:", site]]
    if analyst:
        header.append(["Analyst:", analyst])
    header += [[]] * header_blanks
    records = [*header, *records]

    return records


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rawdir", type=str, default=None, help="raw (output) directory"
    )
    parser.add_argument(
        "--tidydir", type=str, default=None, help="tidy (input) directory"
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
