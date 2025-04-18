# A Laboratory Information Management System

-   [Relational database](g:relational_db) stores data in tables
    -   Usually access with SQL or some variant of it
-   But there are also [document databases](g:document_db)
    -   Sometimes called [NoSQL databases](g:nosql)
-   We will build a (very) simple [laboratory information management system](g:lims) (LIMS)
    using [TinyDB][tinydb]
-   And use [click][click] to build the command-line interface

## Roles and Permissions {: #lims-perms}

-   A user has a [UID](g:uid), a personal name, and a family name
-   A [permission](g:permission) is the right to perform some action
    -   Could give permissions directly to users…
    -   …but experience shows that this becomes unmanageable
-   Instead, create [roles](g:role) that are named collections of permissions and assign roles to users

| Role      | Capability | Scope |
| --------- | ---------- | ----- |
| admin     | view       | all   |
| admin     | upload     | own   |
| admin     | validate   | all   |
| scientist | view       | all   |
| scientist | upload     | own   |
| intern    | view       | own   |

-   Copy data from table of personal and family names
-   First person becomes an admin, second an intern, everyone else a scientist
-   Main driver:

```{data-file="create_db.py:main"}
def main():
    """Main driver."""
    args = parse_args()
    people = get_people(args.sqlite)
    with TinyDB(args.tinydb) as db:
        db.truncate()
        create_capabilities(db)
        create_users(db, people)
        create_roles(db, people)
```

-   Get people from SQL table using a row factory

```{data-file="create_db.py:get_people"}
def get_people(sqlite):
    """Get people from SQLite database."""
    con = sqlite3.connect(sqlite)
    con.row_factory = sqlite3.Row
    rows = con.execute("select personal, family from staff").fetchall()
    return [
        {
            "uid": f"{r['personal'][0].lower()}.{r['family'].lower()}",
            "personal": r["personal"],
            "family": r["family"],
        }
        for r in rows
    ]
```

-   Create capabilities in TinyDB

```{data-file="create_db.py:capabilities"}
CAPABILITIES = [
    {"role": "admin", "capability": "view", "scope": "all"},
    {"role": "admin", "capability": "upload", "scope": "own"},
    {"role": "admin", "capability": "validate", "scope": "all"},
    {"role": "scientist", "capability": "view", "scope": "all"},
    {"role": "scientist", "capability": "upload", "scope": "own"},
    {"role": "intern", "capability": "view", "scope": "own"},
]
```
```{data-file="create_db.py:create_capabilities"}
def create_capabilities(db):
    """Create capabilities in database."""
    capabilities = db.table("capabilities")
    capabilities.truncate()
    for cap in CAPABILITIES:
        capabilities.insert(cap)
```

-   Resulting JSON
    -   Yes, this is really just a rectangular table stored as JSON

```{data-file="capabilities.json"}
{
  "1": {
    "role": "admin",
    "capability": "view",
    "scope": "all"
  },
  "2": {
    "role": "admin",
    "capability": "upload",
    "scope": "own"
  },
  "3": {
    "role": "admin",
    "capability": "validate",
    "scope": "all"
  },
  "4": {
    "role": "scientist",
    "capability": "view",
    "scope": "all"
  },
  "5": {
    "role": "scientist",
    "capability": "upload",
    "scope": "own"
  },
  "6": {
    "role": "intern",
    "capability": "view",
    "scope": "own"
  }
}
```

-   Similar to create people and roles, e.g.:

```{data-file="person.json"}
{
  "uid": "n.bhakta",
  "personal": "Nitya",
  "family": "Bhakta"
}
```

## Actions {: #lims-actions}

-   Create a dataclass to represent assay data

```{data-file="assay_params.py:params"}
@dataclass
class Params:
    """Parameters for assay data."""

    treatment: str = None
    controls: List[str] = field(default_factory=list)
```
```{data-file="assay_params.py:load_params"}
def load_params(filename):
    """Load parameters from file."""
    return Params(**json.loads(Path(filename).read_text()))
```

-   Then create a group of commands with click

```{data-file="lims.py:cli"}
@click.group()
def cli():
    """Interact with laboratory data."""
```

-   Now define a command to upload

```{data-file="lims.py:upload"}
@cli.command()
@click.option("--db", type=str, required=True, help="Database")
@click.option("--assay", type=str, required=True, help="Assay filename")
@click.option("--design", type=str, required=True, help="Design filename")
@click.option("--params", type=str, required=True, help="Parameters filename")
@click.option("--user", type=str, required=True, help="User ID")
def upload(db, user, params, design, assay):
    """Upload design and assay files."""
    params = assay_params.load_params(params)
    design_data = lint.load_file(design)
    assay_data = lint.load_file(assay)
    errors = [
        *lint.lint_design(params, design, design_data),
        *lint.lint_assay(params, assay, assay_data),
    ]
    _require_no_errors(errors)

    with TinyDB(db) as db:
        _require_exists(db, "user", user)
        cap = _get_capability(db, user, "upload")
        _require_cap(cap == "own", f"{user} cannot upload")
        assay_id = _upload_data(db, user, design, assay)
        click.echo(assay_id)
```

-   That's a lot of decorators…
-   Each `@click.option` defines a flag for the `upload` command
-   Run like this

```{data-file="upload.sh"}
python lims.py upload \
	--db lims.json \
	--assay ./assays/fff9b2d6.csv \
	--design ./designs/fff9b2d6.csv \
	--params assays.json \
	--user s.bansal
```

-   Top half of `upload` loads data and checks for errors
    -   Discuss below
-   Bottom half interacts with database
-   Make sure the user exists

```{data-file="lims.py:require_exists"}
def _require_exists(db, kind, value):
    """Check existence of something in database."""
    q = Query()
    match kind:
        case "upload":
            found = db.table("uploads").get(doc_id=value)
            if found is not None:
                return found

        case "user":
            found = db.table("users").search(q.uid == value)
            if len(found) > 1:
                raise ClickException(f"data integrity error: multiple {kind}: {value}")
            if len(found) == 1:
                return found[0]

        case other:
            raise ClickException(f"internal error: unknown kind {kind}")

    raise ClickException(f"No such {kind}: '{value}'")
```

-   Get the user's capabilities

```{data-file="lims.py:get_capability"}
def _get_capability(db, user, kind):
    """Find capability."""
    results = db.table("users").search(Query().uid == user)
    if len(results) != 1:
        raise ClickException(f"unknown user {user}")

    roles = db.table("roles").search(Query().uid == user)
    if len(results) != 1:
        raise ClickException(f"user {user} has no role")
    role = roles[0]["role"]

    q = Query()
    capabilities = db.table("capabilities").search(
        (q.role == role) & (q.capability == kind)
    )
    if not capabilities:
        return None
    if len(capabilities) > 1:
        caps = ", ".join(str(c) for c in capabilities)
        raise ClickException(
            f"duplicate capabilities for user {user} and kind {kind}: {caps}"
        )
    return capabilities[0]["scope"]
```

-   Check that the user has the required capability

```{data-file="lims.py:require_cap"}
def _require_cap(condition, message):
    """Check condition and raise exception."""
    if not condition:
        raise ClickException(f"permission error: {message}")
```

-   *Then* upload the data

```{data-file="lims.py:upload_data"}
def _upload_data(db, user, design_file, assay_file):
    """Upload validated data."""
    timestamp = get_timestamp()
    doc_id = db.table("uploads").insert(
        {"timestamp": timestamp, "uid": user, "design": design_file, "assay": assay_file}
    )
    db.table("status").insert(
        {"upload": doc_id, "uid": user, "status": "created", "timestamp": timestamp}
    )
    return doc_id
```

## Linting {: .lims-lint}

-   Take a closer look at error checking
-   First, get the data as a dataframe

```{data-file="lint.py:load_file"}
def load_file(filename):
    """Load design or assay file as numpy array."""
    return np.loadtxt(filename, delimiter=",", dtype="str")
```

-   Next, build framework for checks

```{data-file="lint.py:lint_assay"}
def lint_assay(params, filename, data):
    """Run checks on a single assay file."""
    return lint_single_file(params, "_lint_assay_", filename, data)
```
```{data-file="lint.py:lint_design"}
def lint_design(params, filename, data):
    """Run checks on a single design file."""
    return lint_single_file(params, "_lint_design_", filename, data)
```
```{data-file="lint.py:lint_single_file"}
def lint_single_file(params, prefix, filename, data):
    """Do one kind of linting on a single set of files."""
    messages = []
    for name, func in globals().items():
        if name.startswith(prefix) and callable(func):
            messages.extend(func(params, filename, data))
    return messages
```

-   Now define functions that do checks
    -   Will be picked up automatically

```{data-file="lint.py:lint_assay_data_shape"}
def _lint_assay_data_shape(params, filename, data):
    """Check shape of assay data."""
    if data.shape != DATA_SHAPE:
        return [f"assay file {filename} has wrong shape {data.shape}"]
    return []
```
```{data-file="lint.py:lint_assay_machine_header"}
def _lint_assay_machine_header(params, filename, data):
    """Check shape of assay data."""
    if data[0, 0] != MACHINE_HEADER:
        return [f"assay file {filename} has wrong machine header {data[0, 0]}"]
    return []
```

## Evaluation {: .lims-eval}

-   What makes this different from "commit data to version control"
    1.  Checking the data on the way in
    2.  Checking that people are authorized to add, view, or update data
-   Is it worth it?
    -   For a single person managing a small set of files: no
    -   For multiple people with many files: absolutely
