"""Utilities."""

import random
import sys

from geopy.distance import lonlat, distance


CIRCLE = 360.0
LON_LAT_PRECISION = 5
READING_PRECISION = 1


def initialize_random(seed=None):
    """Initialize random number generator reproducibly."""
    if seed is None:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    return seed


def random_geo_point(lon, lat, radius):
    """Generate random geo point within radius of center."""
    center = lonlat(lon, lat)
    bearing = random.random() * CIRCLE
    dist = random.random() * radius
    return distance(kilometers=dist).destination((center), bearing=bearing), dist
