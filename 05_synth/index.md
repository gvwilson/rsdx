# Synthesizing Data

## The Problem

-   Synthesize some snails for analysis
    -   Genome: single fixed-length chromosome with a few mutations (for now)
    -   Mass: may depend on mutations
    -   Location: amount of pollution may affect mass as well
-   Want to control statistical properties of specimens to test analysis pipeline

## Introducing Pydantic

-   We mostly don't bother to add type annotations to our code
    -   If we wanted to write Java, we'd write Java…
-   But they *can* be very helpful
-   [Pydantic][pydantic] lets us define [dataclasses](g:dataclass) with [validation](g:validation)

## Synthesis Parameters

[`params_01.py`](./params_01.py)

-   Each [field](g:field) has a name and a type
-   Pydantic will raise an error during construction if a value is not of the right type
-   And provide a description
-   Can also specify constraints like "greater than zero"
-   And define methods to check specialized constraints

## Tests

[`test_params_01.py`](./test_params_01.py)

-   Build an object and check its fields
-   Use the defaults and check against the class definition
    -   Don't have to rewrite this test if field definitions change
-   Use a [parameterized test](g:parameterize_test) to check invalid values
-   In practice, trust Pydantic enough to skip most of these
    -   But always check the hand-crafted validations

## Specimens

-   One Pydantic class to represent specimens
-   Another to represent a collection of specimens and the parameters used to generate them
-   Define [static methods](g:static_method) to construct values
    -   Exercise: use a post-construction method

## More Testing

-   Did you notice that the specimens' genomes are the wrong length?
    -   Using the number of specimens as the length instead of the parameter value
-   *This* is why we test…
-   Mark this test as "expected to fail" because we're not fixing the problem for pedagogical purposes

[`test_specimens_01.py`](./test_specimens_01.py)

## However

-   Running with small sets generates no mutants
    -   Statistically plausible but not helpful for testing our pipeline
-   Change the parameters
    -   Pick one susceptible locus and force higher mutation rate there
-   Can still have populations with no mutants if we want them

## New Parameters

[`params_02.py`](./params_02.py)

-   New `mut_frac` field
-   Constrain upper bound of probabilities as well as lower
    -   Lets us get rid of validator method
-   Add configuration to prevent people accidentally adding more fields
    -   In particular, to prevent [legacy code](g:legacy_code) [failing silently](g:silent_failure)

## Generating Mutants

[`specimens_02.py`](./specimens_02.py)

-   Introduce a [generator](g:generator) for specimen IDs
    -   Declare that it's a [class variable](g:class_variable) so that Pydantic knows not to include it in instances
-   Pick the mutants at the all-specimens level
    -   If a snail is mutant, force the mutation and change the mass
    -   Exercise: why might we wind up with slightly more mutants than we asked for?

## How Do We Test Mutations?

FIXME
