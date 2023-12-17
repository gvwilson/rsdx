"""Run checks on assay data."""

import argparse
from pathlib import Path

import numpy as np

from assay_params import load_params


DATA_SHAPE = (7, 5)
MACHINE_HEADER = "Weyland-Yutani 470"


def main():
    """Main driver."""
    args = parse_args()
    params = load_params(args.params)
    messages = [
        *do_all(args),
        *do_single(params, args.designs, "_lint_design_"),
        *do_single(params, args.assays, "_lint_assay_"),
    ]
    report(messages)


def do_all(args):
    """Do global linting."""
    messages = []
    for name, func in globals().items():
        if name.startswith("_lint_all_") and callable(func):
            messages.extend(func(args))
    return messages


def do_single(params, directory, prefix):
    """Do operations on single set of files."""
    files = {
        filename: np.loadtxt(filename, delimiter=",", dtype="str")
        for filename in Path(directory).iterdir()
    }
    messages = []
    for name, func in globals().items():
        if name.startswith(prefix) and callable(func):
            for filename, array in files.items():
                messages.extend(func(params, filename, array))
    return messages


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--assays", type=str, required=True, help="assay results directory")
    parser.add_argument("--designs", type=str, required=True, help="assay designs directory")
    parser.add_argument("--params", type=str, required=True, help="assay parameters file")
    return parser.parse_args()


def report(messages):
    """Show problems."""
    for m in messages:
        print(m)


def _lint_all_match(args):
    """Do design and result files match 1-1?"""
    design_files = set(p.name for p in Path(args.designs).iterdir())
    assay_files = set(p.name for p in Path(args.assays).iterdir())
    messages = []
    for title, files in (
            ("design but not assay", design_files - assay_files),
            ("assay but not design", assay_files - design_files),
    ):
        if files:
            files = sorted(str(f) for f in files)
            messages.append(f"in {title}: {', '.join(files)}")
    return messages


def _lint_assay_data_shape(params, filename, array):
    """Check shape of assay data."""
    if array.shape != DATA_SHAPE:
        return [f"assay file {filename} has wrong shape {array.shape}"]
    return []


def _lint_assay_machine_header(params, filename, array):
    """Check shape of assay data."""
    if array[0, 0] != MACHINE_HEADER:
        return [f"assay file {filename} has wrong machine header {array[0, 0]}"]
    return []


def _lint_design_data_contents(params, filename, array):
    """Check contents of data portion of file."""
    allowed = {params.treatment} | set(params.controls)
    unknown = set(array[3:7, 1:5].flatten()) - allowed
    if unknown:
        return [f"design file {filename} has unknown value(s) {', '.join(sorted(unknown))}"]
    return []


def _lint_design_data_shape(params, filename, array):
    """Check shape of assay design."""
    if array.shape != DATA_SHAPE:
        return [f"design file {filename} has wrong shape {array.shape}"]
    return []


if __name__ == "__main__":
    main()
