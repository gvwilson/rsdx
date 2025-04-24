"""Generate random persons."""

import random
from typing import ClassVar

import faker
from pydantic import BaseModel, Field
from utils import generic_id_generator


class Person(BaseModel):
    """A single person."""

    id: str = Field(description="unique identifier")
    family: str = Field(description="family name")
    personal: str = Field(description="personal name")

    model_config = {"extra": "forbid"}

    _id_generator: ClassVar = generic_id_generator(lambda i: f"P{i:02d}")

    @staticmethod
    def generate(locale, num):
        """Generate random persons."""
        fake = faker.Faker(locale)
        fake.seed_instance(random.randint(0, 1_000_000))
        return [
            Person(
                id=next(Person._id_generator),
                family=fake.last_name(),
                personal=fake.first_name(),
            )
            for _ in range(num)
        ]

    @staticmethod
    def to_csv(writer, persons):
        """Produce CSV"""
        writer.writerow(["id", "family", "personal"])
        writer.writerows([p.id, p.family, p.personal] for p in persons)
