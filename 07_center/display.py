"""Analyze pollution readings."""

import argparse
import numpy as np
import pandas as pd
import plotly.express as px
import sqlite3
import sys


FIG_SIZE = 800


def main():
    """Main driver."""
    args = parse_args()

    con = sqlite3.connect(args.dbfile)
    sites = pd.read_sql("select * from sites", con)
    surveys = pd.read_sql("select * from surveys", con)
    samples = pd.read_sql("select * from samples", con)

    combined = sites\
        .merge(surveys, how="inner", on="site")\
        .drop(["lon", "lat"], axis=1)\
        .merge(samples, how="inner", on="label")

    for site in sites["site"]:
        rows = combined[combined["site"] == site]
        create_figure(args, site, rows)


def create_figure(args, site, values):
    """Create figure for particular site."""
    center_lon = sum(values["lon"] * values["reading"]) / sum(values["reading"])
    center_lat = sum(values["lat"] * values["reading"]) / sum(values["reading"])

    title = f"{site}: lon={center_lon:.5f} lat={center_lat:.5f}"
    fig = px.scatter(x=values["lon"], y=values["lat"], size=values["reading"], title=title)
    fig.add_vline(x=center_lon)
    fig.add_hline(y=center_lat)
    fig.update_layout(width=FIG_SIZE, height=FIG_SIZE)

    if args.figdir:
        fig.write_image(f"{args.figdir}/{site}.svg")
    else:
        fig.show()


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbfile", type=str, help="database file")
    parser.add_argument("--figdir", type=str, help="figure directory")
    return parser.parse_args()


if __name__ == "__main__":
    main()
