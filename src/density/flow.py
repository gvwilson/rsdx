"""Re-run everything."""

from collections import namedtuple
from metaflow import FlowSpec, Parameter, JSONType, step
import pandas as pd
from invperc import initialize_random, percolate


Args = namedtuple("Args", ["width", "height", "depth", "reps"])
SIZES = [15, 25, 35]
DEPTH = 10
REPS = 20


class InvPercFlow(FlowSpec):
    """Metaflow for invasion percolation."""

    sizes = Parameter("sizes", help="grid sizes", type=JSONType, default=SIZES)
    depth = Parameter("depth", help="grid depth", type=int, default=DEPTH)
    reps = Parameter("reps", help="repetitions", type=int, default=REPS)
    seed = Parameter("seed", help="RNG seed", type=int, required=True)
    save = Parameter("save", help="save as file?", type=bool, default=False)

    @step
    def start(self):
        """Collect parameters and run jobs."""
        initialize_random(self.seed)
        self.args = [
            {
                "args": Args(width=size, height=size, depth=self.depth, reps=self.reps),
                "seed": initialize_random(),
            }
            for size in self.sizes
        ]
        self.next(self.run_job, foreach="args")

    @step
    def run_job(self):
        """Run a sweep with one set of parameters."""
        self.stats = percolate(self.input["args"])
        self.next(self.join)

    @step
    def join(self, inputs):
        """Combine results from all sweeps."""
        self.results = pd.concat([input.stats for input in inputs])
        self.next(self.end)

    @step
    def end(self):
        """Save results."""
        if self.save:
            sizes = "+".join(str(s) for s in self.sizes)
            filename = f"invperc_{sizes}_{self.depth}_{self.seed}.csv"
            with open(filename, "w") as writer:
                print(self.results.to_csv(index=False), file=writer)
        else:
            print(self.results.to_csv(index=False))


if __name__ == "__main__":
    InvPercFlow()
