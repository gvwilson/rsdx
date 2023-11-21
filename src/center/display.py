"""Analyze pollution readings."""

import argparse
import pandas as pd
from pathlib import Path
import plotly.express as px
import sqlite3


FIG_SIZE = 800
Q_SAMPLES = """
select
    surveys.site,
    samples.lon,
    samples.lat,
    samples.reading
from surveys join samples
on surveys.label = samples.label
"""
Q_CENTERS = """
select
    surveys.site,
    sum(samples.lon * samples.reading) / sum(samples.reading) as lon,
    sum(samples.lat * samples.reading) / sum(samples.reading) as lat
from surveys join samples
on surveys.label = samples.label
group by surveys.site
"""


def main():
    """Main driver."""
    args = parse_args()
    tables, final = {}, None
    for method in args.methods:
        final = tables[method] = METHODS[method](args)
    check(args, tables)
    make_figures(args, **final)


def read_csv(args):
    """Read CSV files directly into dataframes."""
    assert args.csvdir, "read_csv requires --csvdir"
    raw = [pd.read_csv(filename) for filename in Path(args.csvdir).glob("*.csv")]
    return combine_with_pandas(args, *raw)


def read_db_pandas(args):
    """Read database tables into Pandas dataframes and manipulate."""
    assert args.dbfile, "read_db_pandas requires --dbfile"
    con = sqlite3.connect(args.dbfile)
    raw = pd.read_sql(Q_SAMPLES, con)
    return combine_with_pandas(args, raw)


def read_db_sql(args):
    """Read tables and do calculations directly in SQL."""
    assert args.dbfile, "read_db_pandas requires --dbfile"
    con = sqlite3.connect(args.dbfile)
    return {
        "combined": pd.read_sql(Q_SAMPLES, con),
        "centers": pd.read_sql(Q_CENTERS, con),
    }


METHODS = {"csv": read_csv, "pandas": read_db_pandas, "sql": read_db_sql}


def combine_with_pandas(args, *tables):
    """Combine tables using Pandas."""
    combined = pd.concat(tables)
    temp = pd.DataFrame(
        {
            "site": combined["site"],
            "weighted_lon": combined["lon"] * combined["reading"],
            "weighted_lat": combined["lat"] * combined["reading"],
            "reading": combined["reading"],
        }
    )
    temp = (
        temp.groupby(["site"])
        .agg({"weighted_lon": "mean", "weighted_lat": "mean", "reading": "mean"})
        .reset_index()
    )
    centers = pd.DataFrame(
        {
            "site": temp["site"],
            "lon": temp["weighted_lon"] / temp["reading"],
            "lat": temp["weighted_lat"] / temp["reading"],
        }
    )
    return {"combined": combined, "centers": centers}


def check(args, tables):
    """Check all tables against each other."""
    reference_key, remaining_keys = args.methods[0], args.methods[1:]
    if not remaining_keys:
        return
    reference = tables[reference_key]
    for other_key in remaining_keys:
        other = tables[other_key]
        assert set(reference.keys()) == set(
            other.keys()
        ), f"Key mis-match {reference_key} {other_key}"
        for name in reference:
            assert len(reference[name]) == len(
                other[name]
            ), f"Length mis-match {reference_key} {other_key} {name}"


def make_figures(args, combined, centers):
    """Create figures showing calculated results."""
    for i, row in centers.iterrows():
        temp = combined[combined["site"] == row["site"]]
        title = f"{row['site']}: lon={row['lon']:.5f} lat={row['lat']:.5f}"
        fig = px.scatter(
            x=temp["lon"], y=temp["lat"], size=temp["reading"], title=title
        )
        fig.add_vline(x=row["lon"])
        fig.add_hline(y=row["lat"])
        fig.update_layout(width=FIG_SIZE, height=FIG_SIZE)
        if args.figdir:
            fig.write_image(f"{args.figdir}/{row['site']}.svg")
            fig.write_image(f"{args.figdir}/{row['site']}.pdf")
        else:
            fig.show()


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--csvdir", type=str, help="CSV directory")
    parser.add_argument("--dbfile", type=str, help="database file")
    parser.add_argument("--figdir", type=str, help="figure directory")
    parser.add_argument(
        "--methods",
        nargs="+",
        type=str,
        help="methods to use",
        choices=list(METHODS.keys()),
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
