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

[%inc params_single.py %]
[%inc standalone.json %]

---

## Getting Started

[%inc flow.py keep=class %]
[%inc flow.py keep=start %]
[%inc flow.py keep=load_params %]

---

## Parameterizing Each Task

[%inc flow.py keep=make_sweeps %]

-   Use nested loops to generate multidmensional "cube" of parameters

---

## Running a Single Job

[%inc flow.py keep=run_job %]

---

## Combining Results

[%inc flow.py keep=join %]

---

## Reporting Results

[%inc flow.py keep=end %]

---

## Running It

-   Run with single-job JSON parameter file shown earlier

[%inc run_standalone.sh %]

-   Run full sweep

[%inc sweep.json %]
[%inc run_sweep.sh %]

---

## But How Does It Work?

FIXME: show how to build a simple DAG-based workflow runner

---

## Exercises

1.  FIXME: add exercises for scaling up

1.  Use recursion to generate parameter sweep for arbitrary number of parameters.
