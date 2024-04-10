---
title: "Scale Up"
tagline: "Generate fractals using a workflow runner and store them remotely."
abstract: >
    Once we have an algorithm that's worth scaling up,
    we need to actually scale it up.
    This lesson shows how to describe a workflow as an acyclic graph,
    how to express that workflow in code to take advantage of cloud computing,
    and how support tools like logging frameworks and remote data storage can help.
syllabus:
-   Describing workflows as directed acyclic graphs.
-   Expressing DAGs in code with Metaflow.
---

-   Reminder: storing parameters as dataclass

[%inc params_single.py %]

-   Load from JSON

[%inc standalone.json %]

-   Build a [%g workflow "workflow" %] to run parameter sweeps using [Metaflow][metaflow]
    -   Define a Python class with methods for workflow stages
    -   Use decorators to mark steps
    -   Parameters to methods coordinate dataflow
-   Start

[%inc flow.py mark=start %]

-   First step loads parameters and creates parameters for each task

[%inc flow.py pattern="class:InvPercFlow meth:start" %]
[%inc flow.py pattern="func:load_params" %]
[%inc flow.py pattern="func:make_sweeps" %]

-   Run a single job

[%inc flow.py pattern="class:InvPercFlow meth:run_job" %]

-   Combine results from all jobs

[%inc flow.py pattern="class:InvPercFlow meth:join" %]

-   Report results

[%inc flow.py pattern="class:InvPercFlow meth:end" %]

-   Run with single-job JSON parameter file shown earlier

[%inc run_standalone.sh %]

-   Run full sweep

[%inc sweep.json %]
[%inc run_sweep.sh %]
