import argparse
import csv
from pathlib import Path
import sqlite3

DETAILS = (
    (
        "assays.csv",
        "assays",
        (
            ("id", "text not null"),
            ("specimen", "text not null"),
            ("machine", "text"),
            ("person", "text"),
            ("row", "integer not null"),
            ("col", "text not null"),
            ("treatment", "text not null"),
            ("reading", "real not null"),
        ),
    ),
    (
        "machines.csv",
        "machines",
        (
            ("id", "text primary key"),
            ("name", "text not null"),
        ),
    ),
    (
        "persons.csv",
        "persons",
        (
            ("id", "text primary key"),
            ("family", "text"),
            ("personal", "text"),
        ),
    ),
    (
        "specimens.csv",
        "specimens",
        (
            ("id", "text primary key"),
            ("genome", "text"),
            ("mass", "real not null"),
        ),
    ),
)


def main():
    """Main driver."""
    args = cmdline_args()
    conn = sqlite3.connect(args.db)
    cursor = conn.cursor()
    source = Path(args.source)
    for filename, tablename, fields in DETAILS:
        rows = read_data(source / filename, fields)
        create_table(cursor, tablename, fields)
        insert_rows(cursor, tablename, fields, rows)
    conn.commit()


def cmdline_args():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True, type=str, help="Output database")
    parser.add_argument("--source", required=True, type=str, help="Source directory")
    return parser.parse_args()


def create_table(cursor, tablename, fields):
    fields = ",\n".join(f"    {f[0]} {f[1]}" for f in fields)
    stmt = f"create table {tablename} (\n{fields}\n)"
    cursor.execute(stmt)


def insert_rows(cursor, tablename, fields, rows):
    fields = ", ".join(["?"] * len(fields))
    stmt = f"insert into {tablename} values({fields})"
    cursor.executemany(stmt, rows)


def read_data(filename, fields):
    """Read data and check against provided fields."""
    with open(filename, "r") as stream:
        rows = [r for r in csv.reader(stream)]
    headers = [f[0] for f in fields]
    err_msg = f"mismatch in {filename}: expected {headers} got {rows[0]}"
    assert len(headers) == len(rows[0]), err_msg
    assert all(x[0] == x[1] for x in zip(headers, rows[0])), err_msg
    return rows[1:]


if __name__ == "__main__":
    main()
