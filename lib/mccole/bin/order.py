"""Show chapter order."""

import sys

import util

if __name__ == "__main__":
    config = util.load_config(sys.argv[1])
    print("\n".join(config.chapters))
