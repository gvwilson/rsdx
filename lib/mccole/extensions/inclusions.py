"""Manage file inclusions."""

from ast import AsyncFunctionDef, ClassDef, FunctionDef, parse, unparse
from pathlib import Path
import textwrap

import ark
import shortcodes

import util


COMMENT = {
    "py": "#",
    "sql": "--",
}


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
    indent = kwargs.get("indent", False)
    try:
        if not kwargs:
            body = _whole(path)
        elif "pattern" in kwargs:
            body = _match(path, kwargs["pattern"], indent)
        elif "mark" in kwargs:
            body = _extract(path, kwargs["mark"], indent)
        else:
            util.fail(f"Badly-formed inclusion for '{path}' in {node} with '{kwargs}'")
        body = f"```{kind}\n{body}\n```\n"
        cls = f'class="language-{kind}"'
        return f'<div {cls} title="{name}" markdown="1">\n{body}</div>'
    except OSError:
        util.fail(f"Unable to read inclusion '{path}' in {node}.")


def _extract(filepath, mark, indent):
    """Extract portion of file in comment markers."""
    if isinstance(filepath, str):
        filepath = Path(filepath)
    text = filepath.read_text()
    suffix = filepath.suffix.lstrip(".")
    if suffix in COMMENT:
        comment = COMMENT[suffix]
        before = f"{comment} [{mark}]"
        after = f"{comment} [/{mark}]"
        before_in = before in text
        after_in = after in text
        if before_in and after_in:
            text = text.split(before)[1].split(after)[0]
        elif before_in or after_in:
            util.fail(
                f"Mis-matched mark with '{mark}' in {filename} in {node.path}"
            )
    return text


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


def _whole(path):
    """Get an entire file."""
    lines = path.read_text().split("\n")
    return textwrap.dedent("\n".join(x.rstrip() for x in lines))
