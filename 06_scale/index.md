# Scaling Up

## The Problem

-   We may need to run hundreds or thousands of simulations to get useful data
    -   The fact that we don't know how many indicates the scale of the problem
-   Build a [workflow](g:workflow) to run parameter sweeps using [Metaflow][metaflow]
    -   Define a Python class with methods for workflow stages
    -   Use decorators to mark steps
    -   Parameters to methods coordinate dataflow

---

## Quick Reminder

-   Store parameters as dataclass

```{data-file="params_single.py"}
"""Parameters for single invasion percolation sweep."""

from dataclasses import dataclass


@dataclass
class ParamsSingle:
    """A single set of invasion percolation parameters."""

    width: int
    height: int
    depth: int
    seed: int = None
```
```{data-file="standalone.json"}
{
    "width": 11,
    "height": 11,
    "depth": 10,
    "seed": 172839
}
```

---

## Getting Started

```{data-file="flow.py:class"}
class InvPercFlow(FlowSpec):
    """Metaflow for invasion percolation."""

    sweep = Parameter("sweep", help="parameter file", type=str, required=True)
```
```{data-file="flow.py:start"}
    @step
    def start(self):
        """Collect parameters and run jobs."""
        sweep = load_params(self.sweep)
        self.args = make_sweeps(sweep)
        self.next(self.run_job, foreach="args")
```
```{data-file="flow.py:load_params"}
def load_params(filename):
    """Get sweep parameters from file."""
    return ParamsSweep(**json.loads(Path(filename).read_text()))
```

---

## Parameterizing Each Task

```{data-file="flow.py:make_sweeps"}
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
```

-   Use nested loops to generate multidmensional "cube" of parameters

---

## Running a Single Job

```{data-file="flow.py:run_job"}
    @step
    def run_job(self):
        """Run a sweep with one set of parameters."""
        grid = invperc(self.input)
        self.result = {
            "size": grid.width(),
            "depth": grid.depth(),
            "density": collect_density(grid),
            "dimension": measure_dimension(grid),
        }
        self.next(self.join)
```

---

## Combining Results

```{data-file="flow.py:join"}
    @step
    def join(self, inputs):
        """Combine results from all sweeps."""
        counts = defaultdict(int)
        dimensions = defaultdict(float)
        densities = defaultdict(list)

        for i in inputs:
            key = (i.result["size"], i.result["depth"])
            counts[key] += 1
            dimensions[key] += i.result["dimension"]
            densities[key].extend(i.result["density"])

        for key in densities:
            densities[key] = estimate_density(densities[key])

        self.results = {
            "counts": counts,
            "dimensions": dimensions,
            "densities": densities,
        }
        self.next(self.end)
```

---

## Reporting Results

```{data-file="flow.py:end"}
    @step
    def end(self):
        """Report results."""
        table = [("size", "depth", "count", "dimension", "density_x", "density_k")]
        for key, count in sorted(self.results["counts"].items()):
            size, depth = key
            dim = self.results["dimensions"][key] / count
            table.append((size, depth, count, dim, *self.results["densities"][key]))
        csv.writer(sys.stdout, lineterminator="\n").writerows(table)
```

---

## Running It

-   Run with single-job JSON parameter file shown earlier

```{data-file="run_standalone.sh"}
python invperc.py standalone.json
```

-   Run full sweep

```{data-file="sweep.json"}
{
    "size": [75, 95, 105],
    "depth": [2, 10, 100],
    "runs": 10,
    "seed": 556677
}
```
```{data-file="run_sweep.sh"}
python flow.py run --sweep sweep.json
```

---

## But How Does It Work?

FIXME: show how to build a simple DAG-based workflow runner

---

## Exercises

1.  FIXME: add exercises for scaling up

1.  Use recursion to generate parameter sweep for arbitrary number of parameters.
