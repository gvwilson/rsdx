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
