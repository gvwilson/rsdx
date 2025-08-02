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


def _specimen_id_generator():
    current = 0
    while True:
        current += 1
        yield f"S{current:06d}"


class Specimen(BaseModel):
    """Store a single specimen specimen."""

    id: str = Field(description="unique ID")
    genome: str = Field(min_length=1, description="genome")
    is_mutant: bool = Field(description="is this a mutant?")
    mass: float = Field(gt=0, description="mass (g)")

    _id_generator: ClassVar = _specimen_id_generator()

    @staticmethod
    def generate(params, ref_genome, is_mutant, susc_locus, susc_base):
        """Generate a single specimen."""

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

        return Specimen(
            id=next(Specimen._id_generator),
            genome="".join(genome),
            is_mutant=is_mutant,
            mass=mass,
        )


class AllSpecimens(BaseModel):
    """Store a set of specimens."""

    params: SpecimenParams = Field(description="generation parameters")
    ref_genome: str = Field(description="reference genome")
    susc_locus: int = Field(description="susceptible locus")
    susc_base: str = Field(description="susceptible mutation")
    samples: list[Specimen] = Field(description="specimens")

    @staticmethod
    def generate(params, num):
        """Generate specimens."""

        if num <= 0:
            raise ValueError(f"invalid number of specimens {num}")

        ref_genome = "".join(random.choices(BASES, k=params.genome_length))
        susc_locus = random.choice(list(range(len(ref_genome))))
        susc_base = random.choice(OTHERS[ref_genome[susc_locus]])

        mutant_ids = set(
            random.choices(list(range(num)), k=math.ceil(params.mut_frac * num))
        )

        samples = [
            Specimen.generate(
                params, ref_genome, i in mutant_ids, susc_locus, susc_base
            )
            for i in range(num)
        ]

        return AllSpecimens(
            params=params,
            ref_genome=ref_genome,
            susc_locus=susc_locus,
            susc_base=susc_base,
            samples=samples,
        )


if __name__ == "__main__":
    random.seed(4217309)
    params = SpecimenParams()
    first = AllSpecimens.generate(params, 3)
    second = AllSpecimens.generate(params, 5)
    print("first", first.samples)
    print("second", second.samples)
