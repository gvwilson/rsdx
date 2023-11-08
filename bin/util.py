"""Utilities."""

from geopy.distance import lonlat, distance
import importlib.util
from pathlib import Path
import random
import sys
import yaml


ARK_FILE = ".ark"
CIRCLE = 360.0
LON_LAT_PRECISION = 5
READING_PRECISION = 1
SNAIL_PRECISION = 2


def initialize_random(seed=None):
    """Initialize random number generator reproducibly."""
    if seed is None:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    return seed


def load_ark_data(dir_path, section=None, default=None):
    """Load .ark file if there, possibly slicing section."""
    path = Path(dir_path, ARK_FILE)
    if not path.exists():
        return default
    with open(path, "r") as reader:
        data = yaml.safe_load(reader)
        return data.get(section, default) if section else data


def load_config(filename):
    """Load configuration file as module."""
    spec = importlib.util.spec_from_file_location("config", filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def random_geo_point(lon, lat, radius):
    """Generate random geo point within radius of center."""
    center = lonlat(lon, lat)
    bearing = random.random() * CIRCLE
    dist = random.random() * radius
    return distance(kilometers=dist).destination((center), bearing=bearing), dist


def source_dirs(src, config, exclude=[]):
    """Generate list of source directories."""
    exclude = set(exclude)
    return [f"{src}/{key}" for key in config.chapters if key not in exclude]


def unpack_args(args, field, *req):
    """Unpack multi-valued command-line argument."""
    value = getattr(args, field)
    assert len(value) == len(req), f"Require {len(req)} arguments for {field}"
    for i, (v, (name, convert, check)) in enumerate(zip(value, req)):
        v = convert(v)
        assert check(v), f"Invalid value {v} for field {i} '{name}' of {field}"
        assert not hasattr(args, name), f"Duplicate field {name} in arguments"
        setattr(args, name, v)
