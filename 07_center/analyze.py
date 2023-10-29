"""Analyze pollution readings."""

import argparse
import pandas as pd
import plotly.express as px
import sys


FIG_SIZE = 800


def main():
    """Main driver."""
    args = parse_args()
    df = pd.read_csv(args.infile) if args.infile else pd.read_csv(sys.stdin)
    center_lon = sum(df["lon"] * df["reading"]) / sum(df["reading"])
    center_lat = sum(df["lat"] * df["reading"]) / sum(df["reading"])
    title = f"Calculated center: lon={center_lon:.5f} lat={center_lat:.5f}"

    fig = px.scatter(df, x="lon", y="lat", size="reading", title=title)
    fig.update_layout(width=FIG_SIZE, height=FIG_SIZE)
    fig.add_vline(x=center_lon)
    fig.add_hline(y=center_lat)

    fig.show()
    if args.outfile:
        fig.write_image(args.outfile)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--infile", type=str, help="input file")
    parser.add_argument("--outfile", type=str, help="output file")
    return parser.parse_args()


if __name__ == "__main__":
    main()
