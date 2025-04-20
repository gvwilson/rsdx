"""Generate random persons."""

import random

import faker
from pydantic import BaseModel, Field
from utils import generic_id_generator


class Person(BaseModel):
    """A single person."""

    id: str = Field(description="unique identifier")
    family: str = Field(description="family name")
    personal: str = Field(description="personal name")

    model_config = {"extra": "forbid"}

    @staticmethod
    def generate(locale, num):
        """Generate random persons."""
        fake = faker.Faker(locale)
        fake.seed_instance(random.randint(0, 1_000_000))
        id_gen = generic_id_generator(lambda i: f"P{i:02d}")
        return [
            Person(id=next(id_gen), family=fake.last_name(), personal=fake.first_name())
            for _ in range(num)
        ]
