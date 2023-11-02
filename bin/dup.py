"""Find duplicate files."""

from collections import defaultdict
import glob
from hashlib import sha256
import os
import sys


def main():
    """Main driver."""
    groups = defaultdict(set)
    for root in sys.argv[1:]:
        for filename in glob.glob(f"{root}/**/*"):
            if not os.path.isfile(filename):
                continue
            data = open(filename, "rb").read()
            hash_code = sha256(data).hexdigest()
            groups[hash_code].add(filename)
    for fileset in groups.values():
        if len(fileset) > 1:
            print(" ".join(sorted(fileset)))


if __name__ == "__main__":
    main()
