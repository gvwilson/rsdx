"""Manage file inclusions."""

from ast import AsyncFunctionDef, ClassDef, FunctionDef, parse, unparse
from pathlib import Path
import textwrap

import ark
import shortcodes

import util


class Match:
    """Represent a single match by kind and name."""

    def __init__(self, cls, name):
        """Construct with one or several classes and a name."""
        self._cls = cls
        self._name = name

    def match(self, node):
        """Return node if a match or None if no match."""
        if isinstance(node, self._cls) and (node.name == self._name):
            return node
        return None


@shortcodes.register("inc")
def inclusion(pargs, kwargs, node):
    """Handle external file inclusion."""
    util.require(
        len(pargs) == 1,
        f"Bad 'inc' shortcode: must have one filename not {pargs}",
    )
    name = pargs[0]
    path = Path(ark.site.config["src_dir"], *node.path) / name
    kind = path.suffix.lstrip(".")
    try:
        if not kwargs:
            body = _include_whole_file(path)
        else:
            body = _include_matching_portion(path, kwargs)
        body = f"```{kind}\n{body}\n```\n"
        cls = f'class="code-sample lang-{kind}"'
        return f'<div {cls} title="{name}" markdown="1">\n{body}</div>'
    except OSError:
        util.fail(f"Unable to read inclusion '{path}' in {node}.")


def _include_matching_portion(path, kwargs):
    """Include matching portion of Python source file."""
    util.require(
        "pattern" in kwargs.keys(), f"Bad 'inc' shortcode: 'pattern' not in {kwargs}"
    )
    pattern = kwargs["pattern"]
    indent = kwargs.get("indent", False)
    return _match(path, pattern, indent)


def _include_whole_file(path):
    """Get an entire file."""
    lines = path.read_text().split("\n")
    return textwrap.dedent("\n".join(x.rstrip() for x in lines))


def _match(filepath, pattern, indent):
    """Match a pattern against the contents of a file."""
    if isinstance(filepath, str):
        filepath = Path(filepath)
    doc = parse(filepath.read_text())
    matchers = _translate_pattern(pattern)
    node = _match_rec(doc, matchers)
    if not node:
        return None
    result = unparse(node)
    if indent:
        result = textwrap.indent(result, " " * node.col_offset)
    return result


def _match_rec(node, exprs):
    """Match recursively, returning node or None."""
    first, rest = exprs[0], exprs[1:]
    for stmt in node.body:
        if found := first.match(stmt):
            return _match_rec(found, rest) if rest else found
    return None


def _translate_pattern(pattern):
    """Turn a pattern into a list of matching objects."""

    lookup = {
        "class": ClassDef,
        "func": (AsyncFunctionDef, FunctionDef),
        "meth": (AsyncFunctionDef, FunctionDef),
    }

    def _translate_one(p):
        cls, name = p.split(":")
        return Match(lookup[cls], name)

    return [_translate_one(p) for p in pattern.split()]
