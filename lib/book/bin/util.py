"""Utilities."""

import importlib.util
from pathlib import Path
import sys
import yaml


INDEX_FILE = "index.md"


def fail(msg):
    """Fail unilaterally."""
    print(msg, file=sys.stderr)
    sys.exit(1)


def get_lint(config):
    """Get a lint setting or empty list."""
    return config.lint if hasattr(config, "lint") else {}


def load_config(filename):
    """Load configuration file as module."""
    spec = importlib.util.spec_from_file_location("config", filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require(cond, msg):
    """Fail if condition untrue."""
    if not cond:
        fail(msg)


def source_dirs(src, config, exclude=[]):
    """Generate list of source directories."""
    exclude = set(exclude)
    return [f"{src}/{key}" for key in config.chapters if key not in exclude]
