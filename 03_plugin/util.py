"""Utilities shared by plugins."""

import pandas as pd

# [query]
# Query to select all samples from database in normalized form.
Q_SAMPLES = """
select
    surveys.site,
    samples.lon,
    samples.lat,
    samples.reading
from surveys join samples
on surveys.label = samples.label
"""
# [/query]


def centers_with_pandas(combined):
    """Find centers of sites."""
    temp = pd.DataFrame(
        {
            "site": combined["site"],
            "weighted_lon": combined["lon"] * combined["reading"],
            "weighted_lat": combined["lat"] * combined["reading"],
            "reading": combined["reading"],
        }
    )
    temp = (
        temp.groupby(["site"])
        .agg({"weighted_lon": "mean", "weighted_lat": "mean", "reading": "mean"})
        .reset_index()
    )
    return pd.DataFrame(
        {
            "site": temp["site"],
            "lon": temp["weighted_lon"] / temp["reading"],
            "lat": temp["weighted_lat"] / temp["reading"],
        }
    )


# [combine_with_pandas]
def combine_with_pandas(*tables):
    """Combine tables using Pandas."""
    combined = pd.concat(tables)
    centers = centers_with_pandas(combined)
    return {"combined": combined, "centers": centers}
# [/combine_with_pandas]
