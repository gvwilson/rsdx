"""Entire scenario."""

import random
from typing import ClassVar
from pydantic import BaseModel, Field
from params import SpecimenParams, ScenarioParams
from grid import Grid, fill_grid
from machines import Machine
from persons import Person
from specimens import AllSnails
from utils import generic_id_generator


class Scenario(BaseModel):
    """Entire synthetic data scenario."""

    params: ScenarioParams = Field(description="scenario parameters")
    grids: dict[str, Grid] = Field(
        default_factory=dict, description="sample site grids"
    )
    specimens: AllSnails = Field(description="all snails")
    sampled: dict[str, tuple[str, tuple[int, int]]] = Field(
        default_factory=dict, description="where specimens taken"
    )
    machines: list[Machine] = Field(
        default_factory=[], description="laboratory machines"
    )
    persons: list[Person] = Field(default_factory=[], description="lab staff")

    model_config = {"arbitrary_types_allowed": True}

    _grid_id_generator: ClassVar = generic_id_generator(lambda i: f"G{i:03d}")

    @staticmethod
    def generate(params):
        """Generate entire scenario."""
        grids = {
            next(Scenario._grid_id_generator): fill_grid(size=params.grid_size)
            for _ in range(params.num_sites)
        }
        specimens = AllSnails.generate(params.specimen_params, params.num_specimens)
        return Scenario(
            params=params,
            grids=grids,
            specimens=specimens,
            sampled=Scenario.sample(params.grid_size, grids, specimens.samples),
            machines=Machine.generate(params.num_machines),
            persons=Person.generate(params.locale, params.num_persons),
        )

    @staticmethod
    def sample(size, grids, specimens):
        """Allocate specimens to grids."""
        coords = {
            gid: [(x, y) for x in range(size) for y in range(size)] for gid in grids
        }
        grid_keys = list(grids.keys())
        result = {}
        for s in specimens:
            gid = random.choice(grid_keys)
            i = random.choice(range(len(coords[gid])))
            result[s.id] = (gid, coords[gid][i])
            del coords[gid][i]
        return result


if __name__ == "__main__":
    params = ScenarioParams(rng_seed=91827364, specimen_params=SpecimenParams())
    scenario = Scenario.generate(params)
    print(scenario)
