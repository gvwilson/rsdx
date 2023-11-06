"""Check configuration."""

import argparse
from pathlib import Path

import util


def main():
    """Main driver."""
    args = parse_args()
    config = util.load_config(args.config)
    for name, func in globals().items():
        if name.startswith("_lint_"):
            func(args, config)


def _lint_chapters_again_keys(args, config):
    """Get chapter keys."""
    expected = set(util.source_dirs(args.src, config))
    actual = {str(p) for p in Path(args.src).glob("*") if p.is_dir()}
    report_diff("chapter keys vs. directories", expected, actual)


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


if __name__ == "__main__":
    main()
