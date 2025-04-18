"""Create empty LIMS database."""

import argparse
import sqlite3

from tinydb import TinyDB


# [capabilities]
CAPABILITIES = [
    {"role": "admin", "capability": "view", "scope": "all"},
    {"role": "admin", "capability": "upload", "scope": "own"},
    {"role": "admin", "capability": "validate", "scope": "all"},
    {"role": "scientist", "capability": "view", "scope": "all"},
    {"role": "scientist", "capability": "upload", "scope": "own"},
    {"role": "intern", "capability": "view", "scope": "own"},
]
# [/capabilities]


# [main]
def main():
    """Main driver."""
    args = parse_args()
    people = get_people(args.sqlite)
    with TinyDB(args.tinydb) as db:
        db.truncate()
        create_capabilities(db)
        create_users(db, people)
        create_roles(db, people)
# [/main]


# [create_capabilities]
def create_capabilities(db):
    """Create capabilities in database."""
    capabilities = db.table("capabilities")
    capabilities.truncate()
    for cap in CAPABILITIES:
        capabilities.insert(cap)
# [/create_capabilities]


def create_roles(db, people):
    """Create roles in database."""
    roles = db.table("roles")
    roles.truncate()
    admin, intern, scientists = people[0], people[1], people[2:]
    roles.insert({"uid": admin["uid"], "role": "admin"})
    roles.insert({"uid": intern["uid"], "role": "intern"})
    for person in scientists:
        roles.insert({"uid": person["uid"], "role": "scientist"})


def create_users(db, people):
    """Create users in database."""
    users = db.table("users")
    users.truncate()
    for person in people:
        users.insert(person)


# [get_people]
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
# [/get_people]


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sqlite", type=str, required=True, help="SQLite database file (input)"
    )
    parser.add_argument(
        "--tinydb", type=str, required=True, help="TinyDB database file (output)"
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
