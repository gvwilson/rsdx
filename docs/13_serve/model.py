"""Execute SQL queries."""

import os
import sqlite3


def get_all(kind):
    """Get all entries of particular kind."""
    conn = sqlite3.connect(os.getenv("RSDX_DB_PATH"))
    if kind == "staff":
        columns = ["ident", "personal", "family"]
        rows = conn.execute("""
            select
                ident,
                personal,
                family
            from staff
        """).fetchall()
    elif kind == "experiments":
        columns = ["ident", "kind", "started", "ended", "num_plates"]
        rows = conn.execute("""
            select
                experiment.ident,
                kind,
                started,
                ended,
                count(*) as num_plates
            from plate join experiment
            on plate.experiment = experiment.ident
            group by experiment.ident
        """).fetchall()
    elif kind == "plates":
        columns = ["ident", "experiment", "uploaded", "invalidated"]
        rows = conn.execute("""
            with invalidated_plates as (
                select distinct plate from invalidated
            )
            select
                ident,
                experiment,
                upload_date as uploaded,
                ident in invalidated_plates as invalidated
            from plate
        """).fetchall()
    else:
        assert False, f"Unknown kind {kind}"
    conn.close()
    return columns, rows


def get_count(kind):
    """How many entries of the given kind?"""
    conn = sqlite3.connect(os.getenv("RSDX_DB_PATH"))
    if kind == "staff":
        result = conn.execute("select count(*) from staff").fetchone()
    elif kind == "experiments":
        result = conn.execute("select count(*) from experiment").fetchone()
    elif kind == "plates":
        result = conn.execute("select count(*) from plate").fetchone()
    else:
        assert False, f"Unknown kind {kind}"
    conn.close()
    return result[0]


def get_plate_filename(plate_id):
    """Where is the plate data stored?"""
    conn = sqlite3.connect(os.getenv("RSDX_DB_PATH"))
    result = conn.execute("select filename from plate where ident = ?", (plate_id,)).fetchone()
    conn.close()
    return result[0] if result else None


if __name__ == "__main__":
    import sys
    if sys.argv[1] == "get_all":
        columns, rows = get_all(sys.argv[2])
        print(columns)
        for r in rows:
            print(r)
    elif sys.argv[1] == "get_count":
        count = get_count(sys.argv[2])
        print(count)
    elif sys.argv[1] == "get_plate_filename":
        loc = get_plate_filename(sys.argv[2])
        print(loc)
    else:
        print(f"unknown choice {sys.argv[1]}", file=sys.stderr)
        sys.exit(1)
