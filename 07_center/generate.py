"""Generate measurement data."""

import argparse
from collections import namedtuple
import pandas as pd
import random
import sqlite3
import sys
from geopy.distance import lonlat, distance


CIRCLE = 360.0
LON_LAT_PRECISION = 5
READING_PRECISION = 1

# Locations.
SITES = pd.DataFrame(
    (
        ("COT", -124.04519, 48.82172),
        ("YOU", -124.19700, 48.87251),
        ("HMB", -124.17555, 48.81673),
        ("GBY", -124.45930, 48.92090),
    ),
    columns=("site", "lon", "lat")
)

# Survey dates and parameters.
SURVEYS = pd.DataFrame(
    (
        (1748, "COT", "2023-04-27", 23, 100.0, 0.10, 0.10),
        (1749, "COT", "2023-04-28", 11, 100.0, 0.10, 0.10),
        (1755, "COT", "2023-05-13", 15, 101.0, 0.11, 0.10),
        (1781, "YOU", "2023-05-01", 12,  90.0, 0.15, 0.15),
        (1790, "HMB", "2023-05-02", 19, 107.0, 0.22, 0.11),
        (1803, "GBY", "2023-05-08",  8,  95.0, 0.10, 0.14),
    ),
    columns=("label", "site", "date", "num", "peak", "relative_sd", "radius")
)


def main():
    """Main driver."""
    args = parse_args()
    all_settings = SITES\
        .set_index("site")\
        .join(SURVEYS.set_index("site"), how="inner")
    all_samples = pd.concat(
        [make_samples(s) for s in all_settings.to_dict(orient="records")]
    )
    create_db(args.dbfile, SITES, SURVEYS, all_samples)


def create_db(filename, sites, surveys, samples):
    """Create database file with all sites and samples."""
    con = sqlite3.connect(filename)
    sites.to_sql("sites", con, index=False, if_exists="replace")
    surveys[["label", "site", "date"]].to_sql("surveys", con, index=False, if_exists="replace")
    samples.to_sql("samples", con, index=False, if_exists="replace")


def make_samples(settings):
    """Generate a set of random points."""
    points = [make_point(settings) for _ in range(settings["num"])]
    samples = pd.DataFrame(points)
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
        "label": settings["label"],
        "lon": point.longitude,
        "lat": point.latitude,
        "reading": expected,
    }


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbfile", type=str, default=None, help="database file")
    parser.add_argument("--seed", type=int, help="RNG seed")
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
