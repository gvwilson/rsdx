"""Show chapter order."""

import sys

import bin_util

config = bin_util.load_config(sys.argv[1])
print("\n".join(config.chapters.keys()))
