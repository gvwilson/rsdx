---
title: "A Lazy Algorithm"
tag: "Doing only as much work as we have to makes our simulation faster."
syllabus:
- FIXME
---

-   Introduce big-oh notation for algorithm performance
-   Keep track of cells on the boundary of the grid to eliminate (or at least reduce) search
    -   Trade space for time
-   Have to fill grid at the start because we want exactly the same random numbers
    -   Instead of generating random cells as we go along, which would be even faster
-   Fix bug in earlier implementations of picking first equally-lowest cell (!)
-   Performance is much (much) better
