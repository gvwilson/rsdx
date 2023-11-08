"""Check configuration."""

import argparse
from collections import defaultdict
import hashlib
from pathlib import Path

import util


def main():
    """Main driver."""
    args = parse_args()
    config = util.load_config(args.config)
    for name, func in globals().items():
        if name.startswith("lint_"):
            func(args, config)


def lint_chapters_again_keys(args, config):
    """Check chapters against chapter keys."""
    expected = set(util.source_dirs(args.src, config))
    actual = {str(p) for p in Path(args.src).glob("*") if p.is_dir()}
    report_diff("chapter keys vs. directories", expected, actual)


def lint_duplicate_files(args, config):
    """Check for duplicated files."""
    source_dirs = {
        Path(d): i for (i, d) in enumerate(util.source_dirs(args.src, config))
    }
    ark_data = {
        src_dir: util.load_ark_data(Path(src_dir), "copied", [])
        for src_dir in source_dirs
    }
    ark_lookup = {
        src_dir: {str(Path(args.src, x)) for x in data}
        for src_dir, data in ark_data.items()
    }
    duplicates = _find_duplicate_files(source_dirs)
    for group in duplicates:
        group = sorted(group, key=lambda filename: source_dirs[filename.parent])
        for i, current in list(enumerate(group))[1:]:
            previous = str(group[i - 1])
            if previous not in ark_lookup[current.parent]:
                print(f"{current} not listed as duplicate of {previous}")
            else:
                ark_lookup[current.parent].remove(previous)
    for src_dir, values in ark_lookup.items():
        if values:
            print(
                f"{src_dir}/{util.ARK_FILE} contains unused {', '.join(sorted(values))}"
            )


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True, help="config file")
    parser.add_argument("--src", type=str, required=True, help="source directory")
    return parser.parse_args()


def report_diff(title, expected, actual):
    """Report mis-matches."""
    if diff := expected - actual:
        print(f"{title} missing: {', '.join(diff)}")
    if diff := actual - expected:
        print(f"{title} extra: {', '.join(diff)}")


def _find_duplicate_files(source_dirs):
    """Group files by duplicate hashes."""
    groups = defaultdict(set)
    for src_dir in source_dirs:
        for path in src_dir.glob("*"):
            if (not path.is_file()) or (str(path).endswith("~")):
                continue
            hash_code = hashlib.sha256(path.read_bytes()).hexdigest()
            groups[hash_code].add(path)
    return [group for group in groups.values() if len(group) > 1]


if __name__ == "__main__":
    main()
