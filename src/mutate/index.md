---
title: "Synthetic Data"
tagline: "Analyze snail genomes to see if a single mutation accounts for size differences."
abstract: >
    In this lesson we pivot from simulation to data analysis
    and build a simple pipeline to find out whether
    a single nucleotide polymorphism can explain differences in
    the sizes of snails in polluted regions.
    We also build a synthetic data generator to help us test our analysis pipeline,
    and use it to show how data analyses can be tested more generally.
syllabus:
-   Use a statistical model of single nucleotide polymorphisms (SNPs) to synthesize genomic data.
-   Use another model to combine that data with geocoded samples to generate snail sizes.
-   Build a program to analyze and visualize the synthetic data to test the analysis pipeline.
---

-   How do you test a data analysis pipeline?
    -   Unit tests of the kind used for invasion percolation aren't necessarily appropriate
    -   Problem isn't the control flow of the code but how it interacts with data
-   [%b Alexander2023 %]: build a [%g synth_data "synthetic data generator" %]
    -   Check the behavior of the pipeline by pushing data with known properties through it
    -   If it finds something statistically significant in white noise, rethink the pipeline
-   [Faker][faker] has tools for generating a lot of useful data (we will use it in future chapters)
-   But it can't generate genomes, so we'll build our own

## Synthesizing Genomes {: #mutate-genome}

-   Create some short snail genomes with [%g snp "single-nucleotide polymorphisms" %]
-   Output will have:
    -   Length: for now, all sequences the same length)
    -   Reference sequence: the unmutated original
    -   Locations: where mutations can occur
    -   Susceptible location and base: which of those locations is the key to variance,
        and what mutated base causes the visible mutation
    -   Individuals: list of generated genomes
-   Since this has multiple fields, store as JSON
-   Main driver

[%inc synthesize_genomes.py pattern=func:main %]

-   Random genomes
    -   Create a random base sequence as the reference genome
    -   Create duplicates for individuals
    -   Determine where SNPs can occur
    -   Introduce significant mutations
    -   Introduce other random mutations
    -   Sort for reproducibility [%b Taschuk2017 %]

[%inc synthesize_genomes.py pattern=func:random_genomes %]

-   Random bases and mutations

[%inc synthesize_genomes.py pattern=func:random_bases %]
[%inc synthesize_genomes.py pattern=func:_mutate_snps %]
[%inc synthesize_genomes.py pattern=func:_mutate_other %]

## Synthesizing Samples {: #mutate-samples}

-   Snail size depends on:
    -   Presence of significant mutation
    -   Distance from epicenter of pollution
-   Building this forces us to be explicit about our model
    -   Variance depends on a single nucleotide
    -   And on linear distance from a center point
-   So:
    -   Load the individuals
    -   Put each individual somewhere near the spill site
    -   Generate a random reading for its size that depends on two factors
-   Main driver should be starting to look familiar

[%inc synthesize_samples.py pattern=func:main %]

-   Get geographic parameters from CSV files
    -   Need to join tables to get longitude, latitude, and nominal pollution radius

[%inc sites.csv %]
[%inc surveys.csv %]
[%inc synthesize_samples.py pattern=func:get_geo_params %]

-   Once we have those, generate location and snail size based on genetics and distance

[%inc synthesize_samples.py pattern=func:generate_samples %]

-   Keep the magic numbers at the top of the file
    -   If we wanted to vary these, would store them as JSON or YAML and load
    -   In particular, would do this if we were sweeping parameters as in [%x scale %]

[%inc synthesize_samples.py mark=parameters %]

## Analysis {: #mutate-analyze }

-   Finally ready to write our analysis
-   Read the CSV data with locations, genomes, and readings
-   Find all candidate locations where sequences don't agree
-   Create a scatter plot by location and base
    -   One showing all data
    -   One showing only locations where there are variations

[% figure
   slug="mutate_all_scatter"
   img="all_data_scatter.svg"
   alt="scatterplot of all readings at all locations"
   caption="Reading as a function of location and base (all)"
%]

[% figure
   slug="mutate_slimmed_scatter"
   img="slimmed_data_scatter.svg"
   alt="scatterplot of all readings at all locations"
   caption="Reading as a function of location and base (all)"
%]

-   Plot reading versus mutation location in ranked order for interesting locations

[% figure
   slug="mutate_slimmed_sorted"
   img="slimmed_data_sorted.svg"
   alt="rank plot of readings at mutation locations"
   caption="Reading as a function of location (rank order)"
%]

-   Clearly a winner in this plot…
-   …but not nearly as clear in scatter plot…
-   …and the winner has only twice the reading of the next-highest (random) value
-   Statistics could tell us if this is what we expect,
    but this isn't a statistics lesson
