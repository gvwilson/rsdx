---
template: slides
title: "Scale Up"
tagline: "Generate fractals using a workflow runner."
abstract: >
    Once we have an algorithm that's worth scaling up,
    we need to actually scale it up.
    This lesson shows how to describe a workflow as an acyclic graph,
    how to express that workflow in code to take advantage of cloud computing.
syllabus:
-   Describing workflows as directed acyclic graphs.
-   Expressing DAGs in code with Metaflow.
---

## The Problem

-   We may need to run hundreds or thousands of simulations to get useful data
    -   The fact that we don't know how many indicates the scale of the problem
-   Build a [%g workflow "workflow" %] to run parameter sweeps using [Metaflow][metaflow]
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

[%inc flow.py mark=start %]
[%inc flow.py pattern="class:InvPercFlow meth:start" %]
[%inc flow.py pattern="func:load_params" %]

---

## Parameterizing Each Task

[%inc flow.py pattern="func:make_sweeps" %]

-   Use nested loops to generate multidmensional "cube" of parameters

---

## Running a Single Job

[%inc flow.py pattern="class:InvPercFlow meth:run_job" %]

---

## Combining Results

[%inc flow.py pattern="class:InvPercFlow meth:join" %]

---

## Reporting Results

[%inc flow.py pattern="class:InvPercFlow meth:end" %]

---

## Running It

-   Run with single-job JSON parameter file shown earlier

[%inc run_standalone.sh %]

-   Run full sweep

[%inc sweep.json %]
[%inc run_sweep.sh %]

---

## But How Does It Work?

[%fixme "show how to build a simple DAG-based workflow runner" %]

---

## Exercises

1.  [%fixme "add exercises for scaling up" %]

1.  Use recursion to generate parameter sweep for arbitrary number of parameters.
