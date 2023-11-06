"""Analyze data from runs."""

import argparse
import numpy as np
import pandas as pd
import plotly.express as px
import sys


def main():
    """Main driver."""
    args = parse_args()
    df = pd.read_csv(args.infile) if args.infile else pd.read_csv(sys.stdin)
    summary = (
        df[["distance_2", "fraction"]]
        .groupby(["distance_2"], as_index=False)
        .agg(func="mean")
    )
    summary["distance"] = np.sqrt(summary["distance_2"])
    print(summary)
    fig = px.line(summary, x="distance", y="fraction")
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
