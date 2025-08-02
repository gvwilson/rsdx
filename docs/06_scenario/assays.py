import random
from typing import ClassVar
from pydantic import BaseModel, Field
from grid import Grid
from utils import PRECISION, generic_id_generator


class Assay(BaseModel):
    """Represent a single assay."""

    id: str = Field(description="unique ID")
    specimen_id: str = Field(description="specimen assayed")
    machine_id: str = Field(description="machine used")
    person_id: str = Field(description="who did assay")
    treatments: Grid = Field(description="treatments applied")
    readings: Grid = Field(description="readings obtained")

    _id_generator: ClassVar = generic_id_generator(lambda i: f"A{i:04d}")

    @staticmethod
    def generate(params, specimen, machine, person):
        """Generate an assay for a specimen."""

        treatments = Assay._make_treatments(params)
        readings = Assay._make_readings(params, specimen, treatments)
        return Assay(
            id=next(Assay._id_generator),
            specimen_id=specimen.id,
            machine_id=machine.id,
            person_id=person.id,
            treatments=treatments,
            readings=readings,
        )

    @staticmethod
    def _make_treatments(params):
        """Generate grid of treatments."""

        grid = Grid(size=params.plate_size)
        for x in range(grid.size):
            for y in range(grid.size):
                grid[x, y] = random.choice("CS")

        return grid

    @staticmethod
    def _make_readings(params, specimen, treatments):
        """Make grid of readings."""
        grid = Grid(size=params.plate_size)
        for x in range(grid.size):
            for y in range(grid.size):
                if treatments[x, y] == "C":
                    mean = 0.0
                elif specimen.is_mutant:
                    mean = params.mean_mutant
                else:
                    mean = params.mean_normal
                grid[x, y] = abs(mean + random.gauss(0, params.noise))

        return grid

    @staticmethod
    def all_csv(writer, assays):
        """Write all assays as a single CSV."""
        writer.writerow(
            [
                "id",
                "specimen",
                "machine",
                "person",
                "row",
                "col",
                "treatment",
                "reading",
            ]
        )
        for a in assays:
            for x in range(a.readings.size):
                for y in range(a.readings.size):
                    writer.writerow(
                        [
                            a.id,
                            a.specimen_id,
                            a.machine_id,
                            a.person_id,
                            y + 1,
                            chr(ord("A") + x),
                            a.treatments[x, y],
                            round(a.readings[x, y], PRECISION),
                        ]
                    )

    def to_csv(self, writer, write_treatments):
        """Save as CSV."""
        padding = [""] * (self.treatments.size - 4)
        for name, value in (
            ("id", self.id),
            ("specimen", self.specimen_id),
            ("machine", self.machine_id),
            ("person", self.person_id),
        ):
            writer.writerow([name, value] + padding)

        if write_treatments:
            grid = self.treatments
            convert = lambda x: x
        else:
            grid = self.readings
            convert = lambda x: round(x, PRECISION)

        title = [""] + [chr(ord("A") + i) for i in range(grid.size)]
        writer.writerow(title)
        for y in range(grid.size):
            row = [f"{y + 1}"] + [convert(grid[x, y]) for x in range(grid.size)]
            writer.writerow(row)
