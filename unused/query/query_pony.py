"""Execute SQL queries using Pony ORM."""

from datetime import date
from prettytable import PrettyTable, MARKDOWN
from pony import orm


db = orm.Database()


class Staff(db.Entity):
    """Staff members."""

    ident = orm.PrimaryKey(int, auto=True)
    personal = orm.Required(str)
    family = orm.Required(str)
    performed = orm.Set("Performed")
    invalidated = orm.Set("Invalidated")


class Experiment(db.Entity):
    """Experiments."""

    ident = orm.PrimaryKey(int, auto=True)
    kind = orm.Required(str)
    started = orm.Required(date)
    ended = orm.Optional(date)
    performed = orm.Set("Performed")
    plates = orm.Set("Plate")


class Performed(db.Entity):
    """Who was involved in which experiments."""

    staff = orm.Required(Staff)
    experiment = orm.Required(Experiment)
    orm.PrimaryKey(staff, experiment)


class Plate(db.Entity):
    """Plates used in experiments."""

    ident = orm.PrimaryKey(int, auto=True)
    experiment = orm.Required(Experiment)
    upload_date = orm.Required(date)
    filename = orm.Required(str, unique=True)
    invalidated = orm.Set("Invalidated")


class Invalidated(db.Entity):
    """Invalidated plates."""

    plate = orm.Required(Plate)
    staff = orm.Required(Staff)
    invalidate_date = orm.Required(date)
    orm.PrimaryKey(plate, staff)


ENTITIES = {
    "staff": Staff,
    "exp": Experiment,
    "plate": Plate,
}


def query_pony(dbfile, action, which=None):
    """Run query and show results."""
    db.bind("sqlite", dbfile, create_db=False)
    db.generate_mapping(create_tables=False)
    with orm.db_session:
        if action == "count":
            return orm.count(e for e in ENTITIES[which])

        elif action == "invalidated":
            tbl = PrettyTable(["name", "plate", "uploaded", "invalidated"])
            tbl.align = "l"
            tbl.set_style(MARKDOWN)
            query = (
                (
                    f"{staff.personal} {staff.family}",
                    plate.ident,
                    plate.upload_date,
                    inv.invalidate_date,
                )
                for staff in Staff
                for perf in Performed
                for plate in Plate
                for inv in Invalidated
                if (staff.ident == perf.staff.ident)
                and (perf.experiment.ident == plate.experiment.ident)
                and (plate.ident == inv.plate.ident)
                and (staff.ident != inv.staff.ident)
            )
            tbl.add_rows(orm.select(query))
            return tbl

        elif action == "ls":
            rows = list(ENTITIES[which].select())
            tbl = PrettyTable(rows[0].to_dict().keys())
            tbl.align = "l"
            tbl.set_style(MARKDOWN)
            tbl.add_rows(r.to_dict().values() for r in rows)
            return tbl
