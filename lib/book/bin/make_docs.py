"""Extract and format docstrings."""

import argparse
import ast
from fnmatch import fnmatch
from pathlib import Path
import sys

import util


def main():
    """Main driver."""
    args = parse_args()
    config = util.load_config(args.config)
    print(f"# {args.title}\n")
    for dirname in util.source_dirs(args.src, config, args.notdirs):
        print(f"## {dirname}\n")
        for filename in Path(dirname).glob("*.py"):
            if any(fnmatch(filename, pat) for pat in args.notfiles):
                continue
            format_file(filename)


def add_parents(root):
    """Add parent members to nodes for later use."""
    for node in ast.walk(root):
        for child in ast.iter_child_nodes(node):
            child.parent = node


def format_entry(filename, thing):
    """Format entry for something."""
    name = filename if isinstance(thing, ast.Module) else thing.name
    ds = ast.get_docstring(thing)
    if ds is None:
        print(f"…{name}", file=sys.stderr)
    if isinstance(thing, ast.Module):
        return f"### `{name}`: {ds}\n"
    if isinstance(thing, ast.ClassDef):
        return f"-   class `{name}`: {ds}"
    assert isinstance(thing, ast.FunctionDef)
    if isinstance(thing.parent, ast.ClassDef):
        return f"    -   method `{name}`: {ds}"
    return f"-   function `{name}`: {ds}"


def format_file(filename):
    """Format contents of file."""
    text = Path(filename).read_text()
    parsed = ast.parse(text)
    add_parents(parsed)
    things = [node for node in ast.walk(parsed) if is_definition(node)]
    for thing in things:
        print(format_entry(filename, thing))
    print()


def is_definition(node):
    """Does this node define something interesting?"""
    return (
        isinstance(node, ast.Module)
        or isinstance(node, ast.FunctionDef)
        or isinstance(node, ast.ClassDef)
    )


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True, help="config file")
    parser.add_argument(
        "--notdirs", type=str, nargs="+", default=[], help="directories to ignore"
    )
    parser.add_argument(
        "--notfiles", type=str, nargs="+", default=[], help="file patterns to ignore"
    )
    parser.add_argument("--src", type=str, required=True, help="source directory")
    parser.add_argument("--title", type=str, required=True, help="page title")
    return parser.parse_args()


if __name__ == "__main__":
    main()
