"""Initialize database with previous experimental data."""

import argparse
from datetime import date, datetime, timedelta
from pathlib import Path
import random
import sqlite3
import string

from faker import Faker

EXPERIMENTS = {
    "calibration": {"staff": [1, 1], "duration": [0, 0], "plates": [1, 1]},
    "trial": {"staff": [1, 2], "duration": [1, 2], "plates": [2, 16]},
}
FILENAME_LENGTH = 8


def main():
    """Main driver."""
    args = parse_args()
    random.seed(args.seed)
    connection = create_tables(args)
    fake = Faker(args.locale)
    for func in [_fill_staff, _fill_experiments]:
        func(args, connection, fake)
    connection.commit()


def _fill_experiments(args, connection, fake):
    """Create experiments and their data."""
    kinds = list(EXPERIMENTS.keys())
    staff_ids = list(range(1, args.staff + 1))
    experiments = []
    performed = []
    plates = []
    for experiment_id in range(1, args.experiments + 1):
        kind = random.choice(kinds)

        started, ended = random_experiment_duration(args, kind)
        experiments.append((kind, round_date(started), round_date(ended)))

        num_staff = random.randint(*EXPERIMENTS[kind]["staff"])
        performed.extend(
            [(experiment_id, s) for s in random.sample(staff_ids, num_staff)]
        )

        if ended is not None:
            plates.extend(random_plates(args, kind, experiment_id, started))

    invalidated = invalidate_plates(args, plates)

    connection.executemany("insert into experiment values (null, ?, ?, ?)", experiments)
    connection.executemany("insert into performed values (?, ?)", performed)
    connection.executemany("insert into plate values (null, ?, ?, ?)", plates)
    connection.executemany("insert into invalidated values (?, ?, ?)", invalidated)


def _fill_staff(args, connection, fake):
    """Create people."""
    data = [(fake.first_name(), fake.last_name()) for _ in range(args.staff)]
    connection.executemany("insert into staff values (null, ?, ?)", data)


def create_tables(args):
    """Create database tables."""
    sql = Path(args.tables).read_text()
    connection = sqlite3.connect(args.dbfile)
    connection.executescript(sql)
    return connection


def invalidate_plates(args, plates):
    """Invalidate a random set of plates."""
    selected = [
        (i, p[1]) for (i, p) in enumerate(plates) if random.random() < args.invalid
    ]
    return [
        (
            plate_id,
            random.randint(1, args.staff + 1),
            random_date_interval(upload_date, args.enddate),
        )
        for (plate_id, upload_date) in selected
    ]


def parse_args():
    """Parse command-line arguments."""

    def _date(s):
        """Format dates."""
        return datetime.strptime(s, "%Y-%m-%d")

    parser = argparse.ArgumentParser()

    parser.add_argument("--dbfile", type=str, required=True, help="database file")
    parser.add_argument(
        "--enddate", type=_date, default="2023-11-10", help="Start date"
    )
    parser.add_argument(
        "--experiments", type=int, default=1, help="Number of experiments"
    )
    parser.add_argument(
        "--invalid", type=float, default=0.1, help="Percentage invalidated plates"
    )
    parser.add_argument("--locale", type=str, default="en_CA", help="locale")
    parser.add_argument("--seed", type=int, required=True, help="RNG seed")
    parser.add_argument("--staff", type=int, default=1, help="Number of staff")
    parser.add_argument(
        "--startdate", type=_date, default="2023-11-01", help="Start date"
    )
    parser.add_argument(
        "--tables", type=str, required=True, help="SQL specification of tables"
    )

    args = parser.parse_args()

    assert 0 <= args.invalid <= 1.0, f"Bad invalid value {args.invalid}"

    return args


def random_experiment_duration(args, kind):
    """Choose random start date and end date for experiment."""
    start = random.uniform(args.startdate.timestamp(), args.enddate.timestamp())
    start = datetime.fromtimestamp(start)
    duration = timedelta(days=random.randint(*EXPERIMENTS[kind]["duration"]))
    end = start + duration
    end = None if end > args.enddate else end
    return start, end


FILENAMES = set([""])


def random_filename():
    """Create a randomized filename."""
    global FILENAMES
    result = ""
    while result in FILENAMES:
        stem = "".join(random.choices(string.hexdigits, k=FILENAME_LENGTH))
        result = f"{stem}.csv"
    FILENAMES.add(result)
    return result


def random_plates(args, kind, experiment_id, start_date):
    """Generate random plate data."""
    return [
        (
            experiment_id,
            random_date_interval(start_date, args.enddate),
            random_filename(),
        )
        for _ in range(random.randint(*EXPERIMENTS[kind]["plates"]))
    ]


def random_date_interval(start_date, end_date):
    """Choose a random end date (inclusive)."""
    if isinstance(start_date, date):
        start_date = datetime(*start_date.timetuple()[:3])
    choice = random.uniform(start_date.timestamp(), end_date.timestamp())
    choice = datetime.fromtimestamp(choice)
    return round_date(choice)


def round_date(raw):
    """Round time to whole day."""
    return None if raw is None else date(*raw.timetuple()[:3])


if __name__ == "__main__":
    main()
