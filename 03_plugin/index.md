# A Plugin Architecture

## The Problem

-   Research data may come from files, databases, websites, and many other sources
-   Instead of adding code to a program to handle each one,
    use a [plugin architecture](g:plugin_architecture)
    to load data handlers dynamically
-   Lets users extend the program without modifying its internals
-   Work backward from configuration file that defines plugin type and its parameters

```{data-file="plugins.json"}
{
    "csv": "../../data/survey_tidy",
    "pandas": "../../data/survey.db",
    "sql": "../../data/survey.db",
    "sqlmodel": "../../data/survey.db"
}
```

---

## Our Data

<figure id="plugin_table_structure">
  <img src="table_structure.svg" alt="Structure of survey tables"/>
  <figcaption>Figure 1: Survey table structure</figcaption>
</figure>

-   Each *site* has a [primary key](g:primary_key) and longitude/latitude
-   Each *survey* has a primary key, a site identifier ([foreign key](g:foreign_key)) and a date
-   Each sample has a site ID foreign key, longitude/latitude, and a reading

---

## Getting Started

-   Write `main`
    -   If the file type is X, load `plugin_X` as a module
    -   Then call the `read_data` function in that module
    -   A [contract](g:contract) between the program and its plugins

```{data-file="display.py:main"}
def main():
    """Main driver."""
    args = parse_args()
    config = json.loads(Path(args.plugins).read_text())
    tables = {}
    for plugin_stem, plugin_param in config.items():
        module = importlib.import_module(f"plugin_{plugin_stem}")
        tables[plugin_stem] = module.read_data(plugin_param)
    check(tables)
    _, values = tables.popitem()
    make_figures(args, values["combined"], values["centers"])
```

-   Result from each `read_data` is a list of tables
    -   Load all available examples to [cross validate](g:cross_validation)

---

## Command Line

-   Parsing command-line arguments is simple

```{data-file="display.py:parse_args"}
def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--figdir", type=str, help="output dir")
    parser.add_argument("--plugins", type=str, required=True, help="config")
    return parser.parse_args()
```

---

## Checking

-   Checking tables against each other
    -   Do they have the same keys?
    -   Do they have the same number of values for each key?

```{data-file="display.py:check"}
def check(tables):
    """Check all tables against each other."""
    ref_key = None
    for key in tables:
        if ref_key is None:
            ref_key = key
            continue
        if set(tables[ref_key].keys()) != set(tables[key].keys()):
            print(f"mis-match in provided tables {ref_key} != {key}")
        else:
            for sub_key in tables[ref_key]:
                if len(tables[ref_key][sub_key]) != len(tables[key][sub_key]):
                    print(f"mis-match in {sub_key}: {ref_key} != {key}")
```

---

## Display

<figure id="plugin-example">
  <img src="./COW.svg" alt="Sample distribution at COW site."/>
  <figcaption>Figure 2: Geographical map of sample distributions around COW site.</figcaption>
</figure>

---

## Handling CSV

-   Plugin to handle CSV is the simplest
    -   Read all the files in the directory using Pandas

```{data-file="plugin_csv.py:read_data"}
def read_data(csvdir):
    """Read CSV files directly into dataframes."""
    raw = [pd.read_csv(filename) for filename in Path(csvdir).glob("*.csv")]
    return util.combine_with_pandas(*raw)
```

-   Concatenate all the tables

```{data-file="util.py:combine_with_pandas"}
def combine_with_pandas(*tables):
    """Combine tables using Pandas."""
    combined = pd.concat(tables)
    centers = centers_with_pandas(combined)
    return {"combined": combined, "centers": centers}
```

---

## Handling Databases

-   Pandas can read directly given a SQL query
-   The simple query

```{data-file="util.py:query"}
# Query to select all samples from database in normalized form.
Q_SAMPLES = """
select
    surveys.site,
    samples.lon,
    samples.lat,
    samples.reading
from surveys join samples
on surveys.label = samples.label
"""
```

---

## Handling Databases

-   The code

```{data-file="plugin_sql.py:read_data"}
def read_data(dbfile):
    """Read tables and do calculations directly in SQL."""
    con = sqlite3.connect(dbfile)
    return {
        "combined": pd.read_sql(util.Q_SAMPLES, con),
        "centers": pd.read_sql(Q_CENTERS, con),
    }
```

---

## Finding Centers

-   The query is more complex, but the code to run it is the same

```{data-file="plugin_sql.py:query"}
Q_CENTERS = """
select
    surveys.site,
    sum(samples.lon * samples.reading) / sum(samples.reading) as lon,
    sum(samples.lat * samples.reading) / sum(samples.reading) as lat
from surveys join samples
on surveys.label = samples.label
group by surveys.site
"""
```

---

## Object-Relational Mapper

-   Use [SQLModel][sqlmodel] [object-relational mapper](g:orm) (ORM)
    -   Define classes using [type annotation](g:type_annotation)
    -   ORM maps these to database columns
-   Hard (odd) part is inter-table relationships
    -   And making sense of error messages

```{data-file="plugin_sqlmodel.py:sites"}
class Sites(SQLModel, table=True):
    """Survey sites."""

    site: str | None = Field(default=None, primary_key=True)
    lon: float
    lat: float
    surveys: list["Surveys"] = Relationship(back_populates="site_id")
```

```{data-file="plugin_sqlmodel.py:surveys"}
class Surveys(SQLModel, table=True):
    """Surveys done."""

    label: int | None = Field(default=None, primary_key=True)
    date: date_type
    site: str | None = Field(default=None, foreign_key="sites.site")
    site_id: Sites | None = Relationship(back_populates="surveys")
    samples: list["Samples"] = Relationship(back_populates="label_id")
```

---

## Reading With an ORM

-   With this, the `read_data` function is:

```{data-file="plugin_sqlmodel.py:read_data"}
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
```

---

## Exercises

1.  Calculate centers using aggregation in ORM.
