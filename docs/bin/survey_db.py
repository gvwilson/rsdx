"""Create SQLite database of survey data."""

import argparse
from pathlib import Path
import sqlite3

import pandas as pd


def main():
    """Main driver."""
    args = parse_args()
    sites, surveys, samples = get_data(args)
    samples = transform(surveys, samples)
    save_data(args, sites, surveys, samples)


def get_data(args):
    """Get data from files."""
    sites = pd.read_csv(Path(args.paramsdir, "sites.csv"))
    surveys = pd.read_csv(Path(args.paramsdir, "surveys.csv"))
    samples = pd.concat([pd.read_csv(f) for f in Path(args.samplesdir).glob("*.csv")])
    return sites, surveys, samples


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbfile", type=str, required=True, help="database file")
    parser.add_argument(
        "--paramsdir", type=str, required=True, help="parameters directory"
    )
    parser.add_argument(
        "--samplesdir", type=str, required=True, help="samples directory"
    )
    return parser.parse_args()


def save_data(args, sites, surveys, samples):
    """Save data in database."""
    con = sqlite3.connect(args.dbfile)
    sites.to_sql("sites", con, index=False, if_exists="replace")
    surveys[["label", "site", "date"]].to_sql(
        "surveys", con, index=False, if_exists="replace"
    )
    samples.to_sql("samples", con, index=False, if_exists="replace")


def transform(surveys, samples):
    """Transform sample data into labelled form."""
    df = surveys.merge(samples, how="inner", on=["site", "date"])
    return df[["label", "lon", "lat", "reading"]]


if __name__ == "__main__":
    main()
