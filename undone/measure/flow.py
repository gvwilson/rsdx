"""Re-run everything."""

from collections import namedtuple
from itertools import product
import random
import numpy as np
import sys

from metaflow import FlowSpec, Parameter, JSONType, step

from invperc import initialize_random, percolate


Args = namedtuple("Args", ["size", "depth", "seed", "job"])
SIZES = [101, 301, 501]
DEPTH = 10
JOBS = 20


class InvPercFlow(FlowSpec):
    """Metaflow for invasion percolation."""

    sizes = Parameter("sizes", help="grid sizes", type=JSONType, default=SIZES)
    depth = Parameter("depth", help="grid depth", type=int, default=DEPTH)
    reps = Parameter("jobs", help="repetitions", type=int, default=JOBS)
    seed = Parameter("seed", help="RNG seed", type=int, required=True)
    save = Parameter("save", help="save as file?", type=bool, default=False)

    @step
    def start(self):
        """Collect parameters and run jobs."""
        initialize_random(self.seed)
        self.args = [
            Args(
                size=size, depth=self.depth, seed=random.randrange(sys.maxsize), job=job
            )
            for size, job in product(self.sizes, range(JOBS))
        ]
        self.next(self.run_job, foreach="args")

    @step
    def run_job(self):
        """Run a simulation with one set of parameters."""
        grid = percolate(self.input)
        size = f"{self.input.size:03d}"
        depth = f"{self.input.depth:02d}"
        job = f"{self.input.job:02d}"
        seed = f"{self.input.seed}"
        filename = f"results/invperc_{size}_{depth}_{job}_{seed}.csv"
        np.savetxt(
            filename, np.array(grid.contents(), dtype=int), fmt="%d", delimiter=","
        )
        self.next(self.join)

    @step
    def join(self, inputs):
        """Join step required by Metaflow."""
        self.next(self.end)

    @step
    def end(self):
        """Wrap up."""
        pass


if __name__ == "__main__":
    InvPercFlow()
