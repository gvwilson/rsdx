"""Laboratory machinery."""

import random
from pydantic import BaseModel, Field


PREFIX = [
    "Aero",
    "Auto",
    "Bio",
    "Centri",
    "Chroma",
    "Cryo",
    "Electro",
    "Fluoro",
    "Hydro",
    "Micro",
    "Nano",
    "Omni",
    "Poly",
    "Pyro",
    "Therma",
    "Ultra",
]

SUFFIX = [
    "Analyzer",
    "Bath",
    "Chamber",
    "Counter",
    "Extractor",
    "Fuge",
    "Incubator",
    "Mixer",
    "Pipette",
    "Probe",
    "Reactor",
    "Reader",
    "Scope",
    "Sensor",
    "Station",
]


class Machine(BaseModel):
    """A piece of experimental machinery."""

    id: str = Field(description="machine ID")
    name: str = Field(description="machine name")

    @staticmethod
    def generate(num):
        """Generate a list of machines."""
        assert num <= len(PREFIX) * len(SUFFIX), f"cannot generate {num} machine names"
        pairs = [(p, s) for p in PREFIX for s in SUFFIX]
        return [
            Machine(id=f"M{i:02d}", name=f"{p} {s}")
            for i, (p, s) in enumerate(random.sample(pairs, k=num))
        ]

    @staticmethod
    def to_csv(writer, machines):
        """Produce CSV"""
        writer.writerow(["id", "name"])
        writer.writerows([m.id, m.name] for m in machines)
