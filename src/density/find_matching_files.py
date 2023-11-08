"""Check that generated files match saved files."""

from collections import defaultdict
import hashlib
from pathlib import Path
import sys


expected = int(sys.argv[1])
seen = defaultdict(set)
for filename in sys.argv[2:]:
    hash_code = hashlib.sha256(Path(filename).read_bytes()).hexdigest()
    seen[hash_code].add(filename)

ok = True
for key, group in seen.items():
    if len(group) == expected:
        continue
    ok = False
    print(key)
    for filename in group:
        print(f"- {filename}")

if ok:
    print("everything is OK")
