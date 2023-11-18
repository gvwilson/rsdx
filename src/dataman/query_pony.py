"""Execute SQL queries using Pony ORM."""

from datetime import date
from prettytable import PrettyTable, MARKDOWN
from pony import orm


db = orm.Database()


class Staff(db.Entity):
    ident = orm.PrimaryKey(int, auto=True)
    personal = orm.Required(str)
    family = orm.Required(str)


class Experiment(db.Entity):
    ident = orm.PrimaryKey(int, auto=True)
    kind = orm.Required(str)
    started = orm.Required(date)
    ended = orm.Optional(date)
    plates = orm.Set("Plate")


class Plate(db.Entity):
    ident = orm.PrimaryKey(int, auto=True)
    experiment_id = orm.Required(Experiment)
    upload_date = orm.Required(date)
    filename = orm.Required(str, unique=True)


ENTITIES = {
    "staff": Staff,
    "exp": Experiment,
    "plate": Plate,
}


def query_pony(dbfile, action, which):
    """Run query and show results."""
    db.bind("sqlite", dbfile, create_db=False)
    db.generate_mapping(create_tables=False)
    with orm.db_session:
        if action == "count":
            result = orm.count(e for e in ENTITIES[which])
            print(result)
        elif action == "ls":
            rows = list(ENTITIES[which].select())
            tbl = PrettyTable(rows[0].to_dict().keys())
            tbl.align = "l"
            tbl.set_style(MARKDOWN)
            tbl.add_rows(r.to_dict().values() for r in rows)
            return tbl
