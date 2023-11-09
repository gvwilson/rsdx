"""Utilities."""

import importlib.util
from pathlib import Path
import sys
import yaml


ARK_FILE = ".ark"


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


def source_dirs(src, config, exclude=[]):
    """Generate list of source directories."""
    exclude = set(exclude)
    return [f"{src}/{key}" for key in config.chapters if key not in exclude]
