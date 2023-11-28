"""Measure fractal dimensions of grids."""

import argparse
from collections import defaultdict

import numpy as np
import pandas as pd
import plotly.express as px


def main():
    """Main driver."""
    args = parse_args()
    fractals = []
    densities = []
    for filename in args.filenames:
        if args.verbose:
            print(f"...{filename}")
        grid = np.loadtxt(filename, dtype=int, delimiter=",")
        for size, ruler, count in measure_dimension(grid):
            fractals.append((filename, size, ruler, count))
        for size, dist_2, fraction in measure_density(grid):
            densities.append((filename, size, dist_2, fraction))

    fractals = pd.DataFrame(fractals, columns=["filename", "size", "ruler", "count"])
    sizes = []
    for sz in list(sorted(set(fractals["size"]))):
        subset = fractals[fractals["size"] == sz]
        dim = -np.polyfit(np.log(subset["ruler"]), np.log(subset["count"]), 1)[0]
        sizes.append((sz, dim))
    sizes = pd.DataFrame(sizes, columns=["size", "dimension"])
    print(sizes.to_csv(index=False))

    densities = pd.DataFrame(
        densities, columns=["filename", "size", "dist_2", "fraction"]
    )
    summary = (
        densities[["size", "dist_2", "fraction"]]
        .groupby(["size", "dist_2"], as_index=False)
        .agg(func="mean")
    )
    summary["distance"] = np.sqrt(summary["dist_2"])
    fig = px.line(summary, x="distance", y="fraction", color="size")
    fig.show()
    if args.densities:
        fig.write_image(args.densities)


def measure_density(grid):
    """Calculate density versus distance from center of grid."""
    assert grid.shape[0] == grid.shape[1]
    size = grid.shape[0]

    cx, cy = size // 2, size // 2
    count_cells = defaultdict(int)
    count_filled = defaultdict(int)
    for x in range(size):
        for y in range(size):
            dist_2 = (x - cx) ** 2 + (y - cy) ** 2
            count_cells[dist_2] += 1
            if grid[x, y] == 0:
                count_filled[dist_2] += 1

    result = [
        (size, dist_2, count_filled[dist_2] / count_cells[dist_2])
        for dist_2 in sorted(count_cells.keys())
    ]
    return result


def measure_dimension(grid):
    """Measure fractal dimension of grid."""
    assert grid.shape[0] == grid.shape[1]
    size = grid.shape[0]

    counts = []
    ruler = 1
    while ruler < size:
        count = 0
        for x in range(size // ruler):
            for y in range(size // ruler):
                count = (
                    count
                    + grid[
                        (x * ruler) : ((x + 1) * ruler), (y * ruler) : ((y + 1) * ruler)
                    ].any()
                )
        counts.append((size, ruler, count))
        ruler *= 2

    return counts


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--densities", required=True, type=str, help="save density counts"
    )
    parser.add_argument("--filenames", nargs="+", help="files to load")
    parser.add_argument(
        "--verbose", action="store_true", default=False, help="print progress"
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
