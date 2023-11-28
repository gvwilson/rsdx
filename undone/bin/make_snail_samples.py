"""Generate samples snails with genomes and locations."""


import argparse
import json
from pathlib import Path
import pandas as pd
import random

from rsdx import util


MIN_SNAIL_SIZE = 0.5
MAX_SNAIL_SIZE = 5.0


def main():
    """Main driver."""
    args = parse_args()
    genomes = json.loads(Path(args.genomes).read_text())
    geo_params = get_geo_params(args)
    samples = generate_samples(args, genomes, geo_params)
    save(args, samples)


def generate_samples(args, genomes, geo_params):
    """Generate snail samples."""
    samples = []
    for sequence in genomes["individuals"]:
        point, distance = util.random_geo_point(**geo_params)
        if sequence[genomes["susceptible_loc"]] == genomes["susceptible_base"]:
            limit = args.positive
        else:
            limit = args.negative
        scale = limit * distance / geo_params["radius"]
        reading = random.uniform(
            MIN_SNAIL_SIZE, MIN_SNAIL_SIZE + MAX_SNAIL_SIZE * scale
        )
        samples.append((point.longitude, point.latitude, sequence, reading))

    df = pd.DataFrame(samples, columns=("lon", "lat", "sequence", "reading"))
    df["lon"] = df["lon"].round(util.LON_LAT_PRECISION)
    df["lat"] = df["lat"].round(util.LON_LAT_PRECISION)
    df["reading"] = df["reading"].round(util.SNAIL_PRECISION)

    return df


def get_geo_params(args):
    """Get geographic parameters."""
    sites = pd.read_csv(Path(args.paramsdir, "sites.csv"))
    surveys = pd.read_csv(Path(args.paramsdir, "surveys.csv"))
    combined = sites.merge(surveys, how="inner", on="site")
    filtered = combined[combined["site"] == args.site].iloc[0]
    return {
        "lon": filtered["lon"],
        "lat": filtered["lat"],
        "radius": filtered["radius"],
    }


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--genomes", type=str, required=True, help="genome file")
    parser.add_argument("--outfile", type=str, help="output file")
    parser.add_argument(
        "--paramsdir", type=str, required=True, help="parameters directory"
    )
    parser.add_argument("--scales", nargs="+", type=float, help="scaling factors")
    parser.add_argument("--site", type=str, required=True, help="site identifier")
    parser.add_argument("--seed", type=int, required=True, help="RNG seed")
    args = parser.parse_args()

    args.seed = util.initialize_random(args.seed)

    util.unpack_args(
        args,
        "scales",
        ("positive", float, lambda x: 0 <= x <= 1.0),
        ("negative", float, lambda x: 0 <= x <= 1.0),
    )

    return args


def save(args, samples):
    """Save or show results."""
    if args.outfile:
        Path(args.outfile).write_text(samples.to_csv(index=False))
    else:
        print(samples.to_csv(index=False))


if __name__ == "__main__":
    main()
