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
        .set_index("site")\
        .join(surveys.set_index("site"), how="inner")\
        .reset_index()\
        .drop(["lon", "lat"], axis=1)\
        .set_index("label")\
        .join(samples.set_index("label"), how="inner")\
        .reset_index()

    for (i, site) in enumerate(sites["site"]):
        temp = combined[combined["site"] == site]
        center_lon = sum(temp["lon"] * temp["reading"]) / sum(temp["reading"])
        center_lat = sum(temp["lat"] * temp["reading"]) / sum(temp["reading"])
        title = f"{site}: lon={center_lon:.5f} lat={center_lat:.5f}"
        fig = px.scatter(x=temp["lon"], y=temp["lat"], size=temp["reading"], title=title)
        fig.add_vline(x=center_lon)
        fig.add_hline(y=center_lat)
        fig.update_layout(width=FIG_SIZE, height=FIG_SIZE)
        fig.show()


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbfile", type=str, help="database file")
    return parser.parse_args()


if __name__ == "__main__":
    main()
