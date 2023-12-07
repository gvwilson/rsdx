"""Find difference between two wordlists."""

import sys


def report(label, words):
    if not words:
        return
    print(label)
    for w in sorted(words):
        print(f"- {w}")


left = {w.strip() for w in sys.stdin.readlines()}
right = {w.strip() for w in open(sys.argv[1], "r").readlines()}
report("unknown", left - right)
report("unused", right - left)
