"""Analyze random snail walks."""

import argparse
import pandas as pd
import plotly.express as px


def main():
    """Main driver."""
    args = parse_args()
    df = pd.read_csv(args.infile)
    filtered = df[df["steps"] == max(df["steps"])]
    fig = px.histogram(filtered, x="initial_dist", y="dosage", nbins=args.nbins)
    fig.show()


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--infile", type=str, required=True, help="input file")
    parser.add_argument("--nbins", type=int, default=10, help="number of bins")
    return parser.parse_args()


if __name__ == "__main__":
    main()
