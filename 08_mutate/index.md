# Synthetic Data

## The Problem

-   How do you test a data analysis pipeline?
    -   Unit tests of the kind used for invasion percolation aren't necessarily appropriate
    -   Problem isn't the control flow of the code but how it interacts with data
-   [Alexander2023](b:Alexander2023): build a [synthetic](g:synth_data)a generator" %]
    -   Check the behavior of the pipeline by pushing data with known properties through it
    -   If it finds something statistically significant in white noise, rethink the pipeline
-   [Faker][faker] has tools for generating a lot of useful data (we will use it in future chapters)
-   But it can't generate genomes, so we'll build our own

FIXME: replace pandas with polars

---

## Synthesizing Genomes

-   Create some short snail genomes with [single](g:snp)leotide polymorphisms" %]
-   Output will have:
    -   Length: for now, all sequences the same length)
    -   Reference sequence: the unmutated original
    -   Locations: where mutations can occur
    -   Susceptible location and base: which of those locations is the key to variance,
        and what mutated base causes the visible mutation
    -   Individuals: list of generated genomes
-   Since this has multiple fields, store as JSON

---

## Main Driver

[%inc synthesize_genomes.py keep=main %]

---

## Random Genomes

-   Create a random base sequence as the reference genome
-   Create duplicates for individuals
-   Determine where SNPs can occur
-   Introduce significant mutations
-   Introduce other random mutations
-   Sort for reproducibility [Taschuk2017](b:Taschuk2017)

---

## Random Genomes

[%inc synthesize_genomes.py keep=random_genomes %]

---

## Random Bases and Mutations

[%inc synthesize_genomes.py keep=random_bases %]
[%inc synthesize_genomes.py keep=mutate_snps %]
[%inc synthesize_genomes.py keep=mutate_other %]

---

## Synthesizing Samples

-   Our model is that snail size depends on:
    -   Presence of significant mutation
    -   Distance from epicenter of pollution
-   Building this forces us to be explicit about our model
    -   Variance depends on a single nucleotide
    -   And on linear distance from a center point
-   So:
    -   Load the individuals
    -   Put each individual somewhere near the spill site
    -   Generate a random reading for its size that depends on two factors

---

## Once More With Feeling

-   Main driver should be starting to look familiar

[%inc synthesize_samples.py keep=main %]

---

## Geography

-   Get geographic parameters from CSV files
-   Need to join tables to get longitude, latitude, and nominal pollution radius

[%inc sites.csv %]
[%inc surveys.csv %]

---

## Geography

[%inc synthesize_samples.py keep=get_geo_params %]

---

## Generate Locations and Sizes

-   Generate location and snail size based on genetics and distance

[%inc synthesize_samples.py keep=generate_samples %]

---

## Magic Numbers

-   Keep the magic numbers at the top of the file
    -   If we wanted to vary these, would store them as JSON or YAML and load
    -   In particular, would do this if we were sweeping parameters as in [the earlier chapter](../06_scale/index.md)

[%inc synthesize_samples.py keep=parameters %]

---

## Analysis

-   Finally ready to write our analysis
-   Read the CSV data with locations, genomes, and readings
-   Find all candidate locations where sequences don't agree
-   Create a scatter plot by location and base
    -   One showing all data
    -   One showing only locations where there are variations

---

## All Our Snails

[% figure
   id="mutate_all_scatter"
   src="all_data_scatter.svg"
   alt="scatterplot of all readings at all locations"
   caption="Reading as a function of location and base (all)"
%]

---

## Snails With Mutations

[% figure
   id="mutate_slimmed_scatter"
   src="slimmed_data_scatter.svg"
   alt="scatterplot of readings for snails with mutations"
   caption="Reading as a function of location and base (mutants)"
%]

---

## Rank Order

[% figure
   id="mutate_slimmed_sorted"
   src="slimmed_data_sorted.svg"
   alt="rank plot of readings at mutation locations"
   caption="Reading as a function of location (rank order)"
%]

---

## Conclusions

-   Clearly a winner in this plot…
-   …but not nearly as clear in scatter plot…
-   …and the winner has only twice the reading of the next-highest (random) value
-   Statistics could tell us if this is what we expect,
    but this isn't a statistics lesson

---

## Exercises

FIXME: create exercises for data analysis chapter
