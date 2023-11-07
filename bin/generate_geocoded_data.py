"""Generate geocoded measurement data."""

import argparse
import pandas as pd
from pathlib import Path
import random
import sqlite3
import sys

import util


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
    columns=("site", "lon", "lat"),
)

# Survey dates and parameters.
SURVEYS = pd.DataFrame(
    (
        (1748, "COT", "2023-04-27", 23, 100.0, 0.10, 0.10),
        (1749, "COT", "2023-04-28", 11, 100.0, 0.10, 0.10),
        (1755, "COT", "2023-05-13", 15, 101.0, 0.11, 0.10),
        (1781, "YOU", "2023-05-01", 12, 90.0, 0.15, 0.15),
        (1790, "HMB", "2023-05-02", 19, 107.0, 0.22, 0.11),
        (1803, "GBY", "2023-05-08", 8, 95.0, 0.10, 0.14),
    ),
    columns=("label", "site", "date", "num", "peak", "relative_sd", "radius"),
)

CSV_QUERY = """\
select site, date, lon, lat, reading
from samples inner join surveys
on samples.label = surveys.label
"""


def main():
    """Main driver."""
    args = parse_args()
    params = pd.DataFrame([{"seed": args.seed}])
    save_params(args, params, SITES, SURVEYS)
    all_settings = SITES.set_index("site").join(SURVEYS.set_index("site"), how="inner")
    all_samples = pd.concat(
        [make_samples(s) for s in all_settings.to_dict(orient="records")]
    )
    create_db(args, params, SITES, SURVEYS, all_samples)
    create_csv(args)


def create_csv(args):
    """Create CSV files from database."""
    if (not args.dbfile) or (not args.csvdir):
        return
    con = sqlite3.connect(args.dbfile)
    df = pd.read_sql(CSV_QUERY, con)
    for site in SITES["site"]:
        subset = df[df["site"] == site]
        subset.to_csv(Path(args.csvdir, f"{site}.csv"), index=False)


def create_db(args, params, sites, surveys, samples):
    """Create database file with all data."""
    if not args.dbfile:
        return
    con = sqlite3.connect(args.dbfile)
    params.to_sql("params", con, index=False, if_exists="replace")
    sites.to_sql("sites", con, index=False, if_exists="replace")
    surveys[["label", "site", "date"]].to_sql(
        "surveys", con, index=False, if_exists="replace"
    )
    samples.to_sql("samples", con, index=False, if_exists="replace")


def make_samples(settings):
    """Generate a set of random points."""
    points = [make_point(settings) for _ in range(settings["num"])]
    samples = pd.DataFrame(points)
    samples["reading"] = samples["reading"].round(READING_PRECISION)
    return samples


def make_point(settings):
    """Make a single sample point."""
    point, dist = util.random_geo_point(settings["lon"], settings["lat"], settings["radius"])
    expected = settings["peak"] * ((settings["radius"] - dist) / settings["radius"])
    sd = expected * settings["relative_sd"]
    reading = abs(random.normalvariate(mu=expected, sigma=sd))
    return {
        "label": settings["label"],
        "lon": point.longitude,
        "lat": point.latitude,
        "reading": reading,
    }


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--csvdir", type=str, default=None, help="CSV directory")
    parser.add_argument("--dbfile", type=str, default=None, help="database file")
    parser.add_argument(
        "--paramsdir", type=str, default=None, help="parameters directory"
    )
    parser.add_argument("--seed", type=int, help="RNG seed")
    args = parser.parse_args()
    args.seed = util.initialize_random(args.seed)
    return args


def save_params(args, params, sites, surveys):
    """Create CSV files."""
    if not args.paramsdir:
        return
    for name, data in (
        ("params", params),
        ("sites", sites),
        ("surveys", surveys),
    ):
        Path(f"{args.paramsdir}/{name}.csv").write_text(data.to_csv(index=False))


if __name__ == "__main__":
    main()
