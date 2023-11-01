"""Work backward from clean CSV to messy CSV for parsing."""

import argparse
import csv
import pandas as pd


COLUMNS = ["site", "date", "lon", "lat", "reading"]
ANALYSTS = [None, "P. Srinath", None]
HEADER_BLANKS = [0, 1, 0, 2]
BODY_INSET = [0, 0, 1]
CAPITALIZE = [False, True, False]


def main():
    """Main driver."""
    args = parse_args()
    sites, surveys, samples = read_clean_data(args)
    combined = sites\
        .drop(["lon", "lat"], axis=1)\
        .merge(surveys, on="site")\
        .merge(samples, on="label")\
        [COLUMNS]
    for (i, site) in enumerate(sorted(set(combined["site"]))):
        records = make_records(
            combined,
            site,
            ANALYSTS[i % len(ANALYSTS)],
            HEADER_BLANKS[i % len(HEADER_BLANKS)],
            BODY_INSET[i % len(BODY_INSET)],
            CAPITALIZE[i % len(CAPITALIZE)]
        )
        write_samples(args, site, records)


def make_records(combined, site, analyst, header_blanks, body_inset, capitalize):
    """Create mangled records as list-of-lists."""
    df = combined[combined["site"] == site]
    records = [
        [row[col] for col in COLUMNS]
        for row in df.to_dict(orient="records")
    ]

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
    parser.add_argument("--clean", type=str, default=None, help="clean directory")
    parser.add_argument("--raw", type=str, default=None, help="raw directory")
    return parser.parse_args()


def read_clean_data(args):
    """Read clean data into dataframes."""
    return [
        pd.read_csv(f"{args.clean}/{stem}.csv")
        for stem in "sites surveys samples".split()
    ]


def write_samples(args, site, records):
    """Write records to file."""
    filename = f"{args.raw}/{site}.csv"
    with open(filename, "w") as writer:
        csv.writer(writer).writerows(records)


if __name__ == "__main__":
    main()
