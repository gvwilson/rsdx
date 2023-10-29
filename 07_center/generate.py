"""Generate measurement data."""

import argparse
from collections import namedtuple
import pandas as pd
import random
import sys
from geopy.distance import lonlat, distance


CIRCLE = 360.0
LON_LAT_PRECISION = 5
READING_PRECISION = 1


def main():
    """Main driver."""
    args = parse_args()
    all_settings = pd.read_csv(args.settings).to_dict(orient="records")
    for settings in all_settings:
        samples = make_samples(settings)
        filename = f"{args.outdir}/{settings['site']}-{settings['date']}.csv"
        with open(filename, "w") as writer:
            writer.write(samples.to_csv(index=False))


def make_samples(settings):
    """Generate a set of random points."""
    points = [make_point(settings) for _ in range(settings["num"])]
    samples = pd.DataFrame(points)
    samples["lon"] = samples["lon"].round(LON_LAT_PRECISION)
    samples["lat"] = samples["lat"].round(LON_LAT_PRECISION)
    samples["reading"] = samples["reading"].round(READING_PRECISION)
    return samples


def make_point(settings):
    """Make a single sample point."""
    center = lonlat(settings["lon"], settings["lat"])
    bearing = random.random() * CIRCLE
    dist = random.random() * settings["radius"]
    point = distance(kilometers=dist).destination((center), bearing=bearing)
    expected = settings["peak"] * ((settings["radius"] - dist) / settings["radius"])
    sd = expected * settings["relative_sd"]
    reading = abs(random.normalvariate(mu=expected, sigma=sd))
    return {
        "site": settings["site"],
        "date": settings["date"],
        "lon": point.longitude,
        "lat": point.latitude,
        "reading": expected,
    }


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=str, default=".", help="output directory")
    parser.add_argument("--seed", type=int, help="RNG seed")
    parser.add_argument("--settings", type=str, required=True, help="settings file")
    args = parser.parse_args()
    args.seed = initialize_random(args.seed)
    return args


def initialize_random(seed=None):
    if seed is None:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    return seed


if __name__ == "__main__":
    main()
