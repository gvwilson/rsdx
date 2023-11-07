"""Show chapter order."""

import sys

import util

config = util.load_config(sys.argv[1])
print("\n".join(config.chapters.keys()))
