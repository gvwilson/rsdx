"""Re-run everything."""

from collections import namedtuple
from metaflow import FlowSpec, Parameter, JSONType, step
import pandas as pd
from pathlib import Path

from invperc import initialize_random, percolate


Args = namedtuple("Args", ["size", "depth", "reps", "verbose"])
SIZES = [15, 25, 35]
DEPTH = 10
REPS = 20


class InvPercFlow(FlowSpec):
    """Metaflow for invasion percolation."""

    sizes = Parameter("sizes", help="grid sizes", type=JSONType, default=SIZES)
    depth = Parameter("depth", help="grid depth", type=int, default=DEPTH)
    reps = Parameter("reps", help="repetitions", type=int, default=REPS)
    seed = Parameter("seed", help="RNG seed", type=int, required=True)
    verbose = Parameter("verbose", help="report progress?", type=bool, default=False)

    @step
    def start(self):
        """Collect parameters and run jobs."""
        initialize_random(self.seed)
        self.args = [
            {
                "args": Args(
                    size=size, depth=self.depth, reps=self.reps, verbose=self.verbose
                ),
                "seed": initialize_random(),
            }
            for size in self.sizes
        ]
        self.next(self.run_job, foreach="args")

    @step
    def run_job(self):
        """Run a sweep with one set of parameters."""
        self.runs, self.results = percolate(self.input["args"])
        self.next(self.join)

    @step
    def join(self, inputs):
        """Combine results from all sweeps."""
        self.all_runs = pd.concat([input.runs for input in inputs])
        self.all_results = pd.concat([input.results for input in inputs])
        self.next(self.end)

    @step
    def end(self):
        """Save results."""
        stem = f"{'+'.join(str(s) for s in self.sizes)}_{self.depth}_{self.reps}_{self.seed}"
        Path(f"results_{stem}.csv").write_text(self.all_results.to_csv(index=False))
        Path(f"runs_{stem}.csv").write_text(self.all_runs.to_csv(index=False))
        print(self.all_runs)


if __name__ == "__main__":
    InvPercFlow()
