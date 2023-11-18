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


def query_direct(action, which, dbfile):
    """Run query and show results."""
    tbl = PrettyTable(COLUMNS[which])
    tbl.align = "l"
    tbl.set_style(MARKDOWN)
    conn = sqlite3.connect(dbfile)
    cursor = conn.execute(QUERIES[action][which])
    tbl.add_rows(cursor.fetchall())
    return tbl
