---
title: "A Lazy Algorithm"
tag: "Doing only as much work as we have to makes our simulation faster."
syllabus:
-   "Introduce concept of big-oh for algorithm performance."
-   "Keep track of cells on the boundary of the grid to reduce search: trade space for time."
-   "Have to fill grid at the start because we want exactly the same random numbers."
-   "Even though generating random cells as we go along would be faster."
-   "Performance is much (much) better: O(1) per filled cell rather than O(N^2)."
-   "Along the way, fix bug in earlier implementations of always picking first equally-lowest cell (biased fractal shape)."
---
