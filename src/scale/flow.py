"""Re-run everything."""

from collections import defaultdict
import json
from pathlib import Path
import random
import sys

from metaflow import FlowSpec, Parameter, JSONType, step

from invperc import invperc
from params_single import ParamsSingle
from params_sweep import ParamsSweep


# Defaults
SIZES = [15, 25, 35]
DEPTH = 10
REPS = 10


class InvPercFlow(FlowSpec):
    """Metaflow for invasion percolation."""

    sweep = Parameter("sweep", help="sweep parameter file", type=str, required=True)

    @step
    def start(self):
        """Collect parameters and run jobs."""
        sweep = load_params(self.sweep)
        self.args = make_sweeps(sweep)
        self.next(self.run_job, foreach="args")

    @step
    def run_job(self):
        """Run a sweep with one set of parameters."""
        grid, num_filled = invperc(self.input)
        self.result = {"size": self.input.width, "num_filled": num_filled, "grid": grid}
        self.next(self.join)

    @step
    def join(self, inputs):
        """Combine results from all sweeps."""
        num_grids = defaultdict(int)
        num_filled = defaultdict(int)
        for i in inputs:
            num_grids[i.result["size"]] += 1
            num_filled[i.result["size"]] += i.result["num_filled"]
        self.results = {"num_grids": num_grids, "num_filled": num_filled}
        self.next(self.end)

    @step
    def end(self):
        """Save results."""
        for size in sorted(self.results["num_grids"].keys()):
            ave = self.results["num_filled"][size] / self.results["num_grids"][size]
            print(f"{size}: {ave:.1f}")


def load_params(filename):
    """Get sweep parameters from file."""
    return ParamsSweep(**json.loads(Path(filename).read_text()))


def make_sweeps(sweeps):
    """Convert sweep parameters into individual jobs."""
    random.seed(sweeps.seed)
    result = []
    for size in sweeps.size:
        for depth in sweeps.depth:
            for run in range(sweeps.runs):
                result.append(
                    ParamsSingle(
                        width=size,
                        height=size,
                        depth=depth,
                        seed=random.randrange(sys.maxsize),
                    )
                )
    return result


if __name__ == "__main__":
    InvPercFlow()
