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

```{data-file="params_01.py"}
from pydantic import BaseModel, Field, model_validator


class SpecimenParams(BaseModel):
    """Parameters for specimen generation."""

    mass_mean: float = Field(default=10.0, gt=0, description="Mean mass")
    mass_sd: float = Field(
        default=1.0, gt=0, description="Relative standard deviation in mass"
    )
    genome_length: int = Field(default=20, gt=0, description="Length of genomes")
    mut_mass_scale: float = Field(
        default=2.0, description="Scaling for mutant snail mass"
    )
    mut_prob: float = Field(
        default=0.05, ge=0, description="Probability of point mutation"
    )

    @model_validator(mode="after")
    def validate_model(self):
        """Validate fields."""

        if self.mut_prob >= 1.0:
            raise ValueError(f"invalid mutation probability {self.mut_prob}")

        return self
```

-   Each [field](g:field) has a name and a type
-   Pydantic will raise an error during construction if a value is not of the right type
-   And provide a description
-   Can also specify constraints like "greater than zero"
-   And define methods to check specialized constraints

## Tests

```{data-file="test_params_01.py"}
import pytest

from params_01 import SpecimenParams


def test_not_defaults():
    fixture = SpecimenParams(
        mass_mean=20.0,
        mass_sd=0.3,
        genome_length=50,
        mut_mass_scale=3.0,
        mut_prob=0.01,
    )
    assert fixture.mass_mean == 20.0
    assert fixture.genome_length == 50
    assert fixture.mut_mass_scale == 3.0
    assert fixture.mass_sd == 0.3
    assert fixture.mut_prob == 0.01


def test_defaults():
    fixture = SpecimenParams()
    for name in SpecimenParams.model_fields:
        assert getattr(fixture, name) == SpecimenParams.model_fields[name].default


@pytest.mark.parametrize(
    ("name", "value"),
    (
        ("mass_mean", -1.0),
        ("mass_sd", -0.5),
        ("genome_length", "string"),
        ("mass_sd", [0.5]),
        ("mut_prob", 100.0),
    ),
)
def test_invalid(name, value):
    with pytest.raises(ValueError):
        SpecimenParams(**{name: value})
```

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

```{data-file="test_specimens_01.py"}
import pytest

from params_01 import SpecimenParams
from specimens_01 import AllSnails


@pytest.mark.xfail
def test_defaults():
    params = SpecimenParams()
    fixture = AllSnails.generate(params, 3)
    assert all(len(s.genome) == params.genome_length for s in fixture.samples)
```

## However

-   Running with small sets generates no mutants
    -   Statistically plausible but not helpful for testing our pipeline
-   Change the parameters
    -   Pick one susceptible locus and force higher mutation rate there
-   Can still have populations with no mutants if we want them

## New Parameters

```{data-file="params_02.py"}
from pydantic import BaseModel, Field


class SpecimenParams(BaseModel):
    """Parameters for specimen generation."""

    mass_mean: float = Field(default=10.0, gt=0, description="Mean mass")
    mass_sd: float = Field(
        default=1.0, gt=0, description="Relative standard deviation in mass"
    )
    genome_length: int = Field(default=20, gt=0, description="Length of genomes")
    mut_mass_scale: float = Field(
        default=2.0, description="Scaling for mutant snail mass"
    )
    mut_frac: float = Field(
        default=0.2, ge=0.0, le=1.0, description="Fraction of significant mutants"
    )
    mut_prob: float = Field(
        default=0.05, ge=0.0, le=1.0, description="Probability of point mutation"
    )

    model_config = {"extra": "forbid"}
```

-   New `mut_frac` field
-   Constrain upper bound of probabilities as well as lower
    -   Lets us get rid of validator method
-   Add configuration to prevent people accidentally adding more fields
    -   In particular, to prevent [legacy code](g:legacy_code) [failing silently](g:silent_failure)

## Generating Mutants

```{data-file="specimens_02.py"}
import math
import random
from typing import ClassVar

from pydantic import BaseModel, Field

from params_02 import SpecimenParams


BASES = "ACGT"
OTHERS = {
    "A": "CGT",
    "C": "AGT",
    "G": "ACT",
    "T": "CGT",
}


def _snail_id_generator():
    current = 0
    while True:
        current += 1
        yield f"S{current:06d}"


class Snail(BaseModel):
    """Store a single snail specimen."""

    id: str = Field(description="unique ID")
    genome: str = Field(min_length=1, description="genome")
    is_mutant: bool = Field(description="is this a mutant?")
    mass: float = Field(gt=0, description="mass (g)")

    _id_generator: ClassVar = _snail_id_generator()

    @staticmethod
    def generate(params, ref_genome, is_mutant, susc_locus, susc_base):
        """Generate a single snail."""

        genome = [
            random.choice(OTHERS[b])
            if random.uniform(0.0, 1.0) < params.mut_prob
            else b
            for i, b in enumerate(ref_genome)
        ]
        mass = abs(random.gauss(params.mass_mean, params.mass_sd))

        if is_mutant:
            genome[susc_locus] = susc_base
            mass *= params.mut_mass_scale

        return Snail(
            id=next(Snail._id_generator),
            genome="".join(genome),
            is_mutant=is_mutant,
            mass=mass,
        )


class AllSnails(BaseModel):
    """Store a set of snails."""

    params: SpecimenParams = Field(description="generation parameters")
    ref_genome: str = Field(description="reference genome")
    susc_locus: int = Field(description="susceptible locus")
    susc_base: str = Field(description="susceptible mutation")
    samples: list[Snail] = Field(description="snails")

    @staticmethod
    def generate(params, num):
        """Generate snails."""

        if num <= 0:
            raise ValueError(f"invalid number of snails {num}")

        ref_genome = "".join(random.choices(BASES, k=params.genome_length))
        susc_locus = random.choice(list(range(len(ref_genome))))
        susc_base = random.choice(OTHERS[ref_genome[susc_locus]])

        mutant_ids = set(
            random.choices(list(range(num)), k=math.ceil(params.mut_frac * num))
        )

        samples = [
            Snail.generate(params, ref_genome, i in mutant_ids, susc_locus, susc_base)
            for i in range(num)
        ]

        return AllSnails(
            params=params,
            ref_genome=ref_genome,
            susc_locus=susc_locus,
            susc_base=susc_base,
            samples=samples,
        )


if __name__ == "__main__":
    random.seed(4217309)
    params = SpecimenParams()
    first = AllSnails.generate(params, 3)
    second = AllSnails.generate(params, 5)
    print("first", first.samples)
    print("second", second.samples)
```

-   Introduce a [generator](g:generator) for specimen IDs
    -   Declare that it's a [class variable](g:class_variable) so that Pydantic knows not to include it in instances
-   Pick the mutants at the all-specimens level
    -   If a snail is mutant, force the mutation and change the mass
    -   Exercise: why might we wind up with slightly more mutants than we asked for?

## How Do We Test Mutations?

FIXME
