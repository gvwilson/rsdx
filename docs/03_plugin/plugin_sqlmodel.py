"""Read data using SQLModel ORM."""

from datetime import date as date_type
import pandas as pd
from typing import Optional
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
import util


# [sites]
class Sites(SQLModel, table=True):
    """Survey sites."""

    site: str | None = Field(default=None, primary_key=True)
    lon: float
    lat: float
    surveys: list["Surveys"] = Relationship(back_populates="site_id")
# [/sites]


# [surveys]
class Surveys(SQLModel, table=True):
    """Surveys done."""

    label: int | None = Field(default=None, primary_key=True)
    date: date_type
    site: str | None = Field(default=None, foreign_key="sites.site")
    site_id: Sites | None = Relationship(back_populates="surveys")
    samples: list["Samples"] = Relationship(back_populates="label_id")
# [/surveys]


class Samples(SQLModel, table=True):
    """Individual samples."""

    rowid: int | None = Field(default=None, primary_key=True)
    lon: float
    lat: float
    reading: float
    label: str | None = Field(default=None, foreign_key="surveys.label")
    label_id: Surveys | None = Relationship(back_populates="samples")


# [read_data]
def read_data(dbfile):
    """Read database and do calculations with SQLModel ORM."""
    url = f"sqlite:///{dbfile}"
    engine = create_engine(url)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        combined = list(
            (s.label_id.site, s.lon, s.lat, s.reading)
            for s in session.exec(select(Samples))
        )
        combined = pd.DataFrame(
            combined,
            columns=["site", "lon", "lat", "reading"]
        )
        return {
            "combined": combined,
            "centers": util.centers_with_pandas(combined)
        }
# [/read_data]
