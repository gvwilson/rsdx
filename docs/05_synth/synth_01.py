from pydantic import BaseModel, Field, model_validator


class SpecimenParams(BaseModel):
    """Parameters for specimen generation."""

    mean_mass: float = Field(default=10.0, gt=0, description="Mean mass")
    genome_length: int = Field(default=20, gt=0, description="Length of genomes")
    mut_mass_scale: float = Field(
        default=2.0, description="Scaling for mutant snail mass"
    )
    mass_rel_sd: float = Field(
        default=0.5, gt=0, description="Relative standard deviation in mass"
    )
    p_mutation: float = Field(
        default=0.05, ge=0, description="Probability of point mutation"
    )

    @model_validator(mode="after")
    def validate_model(self):
        """Validate fields."""

        if self.mut_mass_scale < 1.0:
            raise ValueError(f"invalid mass scale factor {self.mut_mass_scale}")

        if self.p_mutation >= 1.0:
            raise ValueError(f"invalid probability of mutation {self.p_mutation}")

        return self
