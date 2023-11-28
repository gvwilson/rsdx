"""Analyze data from runs."""

import argparse
import pandas as pd
import plotly.express as px
import sys


def main():
    """Main driver."""
    args = parse_args()
    df = pd.read_csv(f"{args.stem}.csv") if args.stem else pd.read_csv(sys.stdin)
    summary = (
        df[["kind", "width", "time"]]
        .groupby(["kind", "width"], as_index=False)
        .agg(func="mean")
    )
    print(summary)
    fig = px.line(summary, x="width", y="time", color="kind")
    fig.show()
    fig.write_image(f"{args.stem}.svg")
    fig.write_image(f"{args.stem}.pdf")


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--stem", type=str, help="file stem")
    return parser.parse_args()


if __name__ == "__main__":
    main()
