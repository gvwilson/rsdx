# Introduction

## The Problem

-   Most research software engineers are self-taught programmers
-   Often have gaps in their knowledge
-   One of those gaps is software design
-   A large program is more than just a dozen small programs

<figure id="intro-complexity">
  <img src="complexity.svg" alt="Complexity and size"/>
  <figcaption>Figure 1: How complexity grows with size.</figcaption>
</figure>

## Comprehension

<figure id="intro-comprehension">
  <img src="comprehension.svg" alt="Abstract vs. comprehension"/>
  <figcaption>Figure 2: Abstraction vs. comprehension for novices and experts.</figcaption>
</figure>

-   Experts understand lower and higher abstraction levels than novices
-   Preferred level shifts right with experience
    -   Code that is optimal for one reader may not be optimal for another
-   Most programming language features and programming practices exist to manage complexity

## How to Learn Design

-   Best way to learn design is from examples ([Petre2016](b:Petre2016)]
-   These lessons use small versions of common research problems
    -   Generally accessible to people who are programming
    -   Introduce some fundamental ideas in computer science

## Scenario

-   Years ago,
    logging companies dumped toxic waste in a remote region of Vancouver Island
-   As the containers leaked and the pollution spread,
    some of the tree snails in the region began growing unusually large
-   Your team is going to collect and analyze specimens from affected regions
    to determine if a mutant gene makes snails more susceptible to the pollution
-   Your task is to build a [synthetic data generator](g:synth_data) [[Alexander2023](b:Alexander2023)]
    so that the data scientists can start building and validating analysis pipelines

## Who You Are

-   Maya has a master's degree in genomics
    -   Knows enough Python to analyze data from her experiments
    -   Struggling to write code other people can use
-   These lessons will teach her how to design, build, and test large programs
    in less time and with less pain

## What You Already Know

-   Write Python programs using lists, loops, conditionals, dictionaries, and functions
-   Puzzle through Python programs that use classes and decorators
-   Comfortable using the Unix command line (`cd`, `ls`, `mv`)
-   Read and write a little bit of HTML
-   Use Git to save and share files (`add`, `commit`, `push`, `pull`, `log`)

## Details

-   Written material: [Creative Commons - Attribution - NonCommercial][cc_by_nc] license
-   Code: [Hippocratic License][hippocratic_license]
-   Source available in [Git repository][lesson_repo]
-   Can all be read [online][lesson_site]

## The Author

[**Greg Wilson**][third_bit]
has worked in industry and academia for 40 years,
and is the author, co-author, or editor of over a dozen previous books.
He was the co-founder and first Executive Director of [Software Carpentry][carpentries]
and received ACM SIGSOFT's Influential Educator Award in 2020.
