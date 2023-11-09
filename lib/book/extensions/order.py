"""Show chapter order."""

import sys

import bin_util

if __name__ == "__main__":
    config = bin_util.load_config(sys.argv[1])
    print("\n".join(config.chapters))
