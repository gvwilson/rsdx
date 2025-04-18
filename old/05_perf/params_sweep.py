"""Parameters for invasion percolation sweep."""

from dataclasses import dataclass


# [paramssweep]
@dataclass
class ParamsSweep:
    """A range of invasion percolation parameters."""

    kind: list[str]
    size: list[int]
    depth: list[int]
    runs: int
    seed: int = None
# [/paramssweep]
