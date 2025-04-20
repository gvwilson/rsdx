import random
from pydantic import BaseModel, Field
from params_01 import SpecimenParams


BASES = "ACGT"
OTHERS = {
    "A": "CGT",
    "C": "AGT",
    "G": "ACT",
    "T": "CGT",
}
SPECIMEN_ID = 0


class Specimen(BaseModel):
    """Store a single snail specimen."""

    id: str = Field(description="unique ID")
    genome: str = Field(min_length=1, description="genome")
    mass: float = Field(gt=0, description="mass (g)")

    @staticmethod
    def generate(params, ref_genome):
        """Generate a single specimen."""

        global SPECIMEN_ID
        SPECIMEN_ID += 1
        genome = "".join(
            random.choice(OTHERS[b])
            if random.uniform(0.0, 1.0) < params.mut_prob
            else b
            for i, b in enumerate(ref_genome)
        )
        mass = abs(random.gauss(params.mass_mean, params.mass_sd))
        return Specimen(id=f"S{SPECIMEN_ID:06d}", genome=genome, mass=mass)


class AllSpecimens(BaseModel):
    """Store a set of specimens."""

    params: SpecimenParams = Field(description="generation parameters")
    ref_genome: str = Field(description="reference genome")
    samples: list[Specimen] = Field(description="specimens")

    @staticmethod
    def generate(params, num):
        """Generate specimens."""

        if num <= 0:
            raise ValueError(f"invalid number of specimens {num}")

        ref_genome = "".join(random.choices(BASES, k=num))
        return AllSpecimens(
            params=params,
            ref_genome=ref_genome,
            samples=[Specimen.generate(params, ref_genome) for _ in range(num)],
        )


if __name__ == "__main__":
    random.seed(4217309)
    params = SpecimenParams()
    first = AllSpecimens.generate(params, 3)
    second = AllSpecimens.generate(params, 5)
    print("first", first)
    print("second", second)
