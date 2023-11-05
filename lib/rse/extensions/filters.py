"""Filters for use in template expansion."""

import ibis
import util


@ibis.filters.register("is_root")
def is_root(node):
    """Is this the root node?"""
    return len(node.path) == 0


@ibis.filters.register("not_root")
def not_root(node):
    """Is this _not_ the root node?"""
    return not is_root(node)


@ibis.filters.register("part_title")
def part_title(node):
    """Insert chapter title."""
    return util.get_title(node)
