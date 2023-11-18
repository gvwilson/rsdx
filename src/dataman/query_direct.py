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
        "plate": "select ident, experiment_id, upload_date from plate",
    },
}


def query_direct(dbfile, action, which):
    """Run query and show results."""
    conn = sqlite3.connect(dbfile)

    if action == "count":
        count = conn.execute(QUERIES[action][which]).fetchone()[0]
        return count

    elif action == "ls":
        tbl = PrettyTable(COLUMNS[which])
        tbl.align = "l"
        tbl.set_style(MARKDOWN)
        tbl.add_rows(conn.execute(QUERIES[action][which]).fetchall())
        return tbl

    else:
        assert False, f"unknown action {action}"
