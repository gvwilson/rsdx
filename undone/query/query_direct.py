"""Execute SQL queries directly."""

from prettytable import PrettyTable, MARKDOWN
import sqlite3


COLUMNS = {
    "staff": ["ident", "personal", "family"],
    "exp": ["ident", "kind", "started", "ended"],
    "plate": ["ident", "experiment", "uploaded"],
}

QUERIES = {
    "count": {
        "staff": "select count(*) from staff",
        "exp": "select count(*) from experiment",
        "plate": "select count(*) from plate",
    },
    "ls": {
        "staff": "select * from staff",
        "exp": "select * from experiment",
        "plate": "select ident, experiment, upload_date from plate",
    },
}

INVALIDATED_QUERY = """\
select staff.personal || " " || staff.family, plate.ident, plate.upload_date, invalidated.invalidate_date
from staff inner join performed inner join plate inner join invalidated
on (staff.ident = performed.staff)
    and (performed.experiment = plate.experiment)
    and (plate.ident = invalidated.plate)
    and (invalidated.staff != staff.ident)
"""


def query_direct(dbfile, action, which=None):
    """Run query and show results."""
    conn = sqlite3.connect(dbfile)

    if action == "count":
        assert which is not None
        count = conn.execute(QUERIES[action][which]).fetchone()[0]
        return count

    elif action == "invalidated":
        tbl = PrettyTable(["name", "plate", "uploaded", "invalidated"])
        tbl.align = "l"
        tbl.set_style(MARKDOWN)
        tbl.add_rows(conn.execute(INVALIDATED_QUERY))
        return tbl

    elif action == "ls":
        assert which is not None
        tbl = PrettyTable(COLUMNS[which])
        tbl.align = "l"
        tbl.set_style(MARKDOWN)
        tbl.add_rows(conn.execute(QUERIES[action][which]).fetchall())
        return tbl

    else:
        assert False, f"unknown action {action}"
