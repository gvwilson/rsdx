"""Check configuration."""

import argparse
from pathlib import Path
import yaml

import util


def main():
    """Main driver."""
    args = parse_args()
    config = util.load_config(args.config)
    for name, func in globals().items():
        if name.startswith("_lint_"):
            func(args, config)


def _lint_chapters_again_keys(args, config):
    """Check chapters against chapter keys."""
    expected = set(util.source_dirs(args.src, config))
    actual = {str(p) for p in Path(args.src).glob("*") if p.is_dir()}
    report_diff("chapter keys vs. directories", expected, actual)


def _lint_copied_files(args, config):
    """Check carry-forward files."""
    for src_dir in util.source_dirs(args.src, config):
        ark_file = Path(src_dir, ".ark")
        if not ark_file.exists():
            continue
        with open(ark_file, "r") as reader:
            ark_data = yaml.safe_load(reader)
        for (local, original) in ark_data.get("copy", {}).items():
            local_path = Path(src_dir, local)
            original_path = Path(args.src, original)
            if local_path.read_text() != original_path.read_text():
                print(f"{local_path} != {original_path}")


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
