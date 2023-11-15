"""Generate geocoded measurement data."""

import argparse
import pandas as pd
from pathlib import Path
import random
import sqlite3

from rsdx import util


def main():
    """Main driver."""
    args = parse_args()

    sites = pd.read_csv(Path(args.paramsdir, "sites.csv"))
    surveys = pd.read_csv(Path(args.paramsdir, "surveys.csv"))

    util.initialize_random(args.seed)

    settings = sites.set_index("site").join(surveys.set_index("site"), how="inner")
    samples = pd.concat([make_samples(s) for s in settings.to_dict(orient="records")])
    samples["lon"] = samples["lon"].round(util.LON_LAT_PRECISION)
    samples["lat"] = samples["lat"].round(util.LON_LAT_PRECISION)

    create_db(args, sites, surveys, samples)
    create_csv(args, sites, surveys, samples)


def create_csv(args, sites, surveys, samples):
    """Create tidy sample CSV files."""
    if not args.csvdir:
        return
    df = surveys.merge(samples, how="inner", on="label")
    for site in sites["site"]:
        subset = df[df["site"] == site][["site", "date", "lon", "lat", "reading"]]
        subset.to_csv(Path(args.csvdir, f"{site}.csv"), index=False)


def create_db(args, sites, surveys, samples):
    """Create database file with all data."""
    if not args.dbfile:
        return
    con = sqlite3.connect(args.dbfile)
    sites.to_sql("sites", con, index=False, if_exists="replace")
    surveys[["label", "site", "date"]].to_sql(
        "surveys", con, index=False, if_exists="replace"
    )
    samples.to_sql("samples", con, index=False, if_exists="replace")


def make_samples(settings):
    """Generate a set of random points."""
    points = [make_point(settings) for _ in range(settings["num"])]
    samples = pd.DataFrame(points)
    samples["reading"] = samples["reading"].round(util.READING_PRECISION)
    return samples


def make_point(settings):
    """Make a single sample point."""
    point, dist = util.random_geo_point(
        settings["lon"], settings["lat"], settings["radius"]
    )
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
    parser.add_argument("--seed", required=True, type=int, help="RNG seed")
    args = parser.parse_args()
    args.seed = util.initialize_random(args.seed)
    return args


if __name__ == "__main__":
    main()
