"""Make HTML pages for assay staff for scraping."""

import argparse
from collections import defaultdict
from jinja2 import Template
from pathlib import Path
import random
import sqlite3

from faker import Faker

from assay_params import load_params


BIO_LENGTH = 4
TITLE = "Northwest Clamatsin Snail Project"
COPYRIGHT = "Copyright (c) 2023"
EXPERIMENT_QUERY = """\
select staff.ident, experiment.kind, count(*)
from staff inner join performed inner join experiment
on staff.ident = performed.staff
and performed.experiment = experiment.ident
group by staff.ident, experiment.kind;
"""
STAFF_QUERY = """\
select staff.ident, staff.personal, staff.family from staff
"""


def main():
    """Main driver."""
    args = parse_args()
    random.seed(args.seed)
    params = load_params(args.params)

    index_template = Template(Path(args.index).read_text())
    staff_template = Template(Path(args.staff).read_text())

    fake = Faker(params.locale)
    connection = sqlite3.connect(args.dbfile)

    staff = {
        ident: {"personal": personal, "family": family, "bio": make_paragraphs(fake)}
        for (ident, personal, family) in connection.execute(STAFF_QUERY).fetchall()
    }
    for s in staff.values():
        s["page"] = make_staff_page_name(s)

    experiments = defaultdict(dict)
    for ident, kind, count in connection.execute(EXPERIMENT_QUERY).fetchall():
        experiments[ident][kind] = count

    content = index_template.render(
        data={
            "title": TITLE,
            "copyright": COPYRIGHT,
            "staff": staff,
        }
    )
    Path(args.pagedir, "index.html").write_text(content)

    for ident in staff:
        filename = Path(args.pagedir, staff[ident]["page"])
        content = staff_template.render(
            data={
                "staff": staff[ident],
                "experiments": experiments[ident],
                "title": TITLE,
                "copyright": COPYRIGHT,
            }
        )
        filename.write_text(content)


def make_paragraphs(fake):
    """Generate fake biography."""
    return fake.paragraph(nb_sentences=BIO_LENGTH)


def make_staff_page_name(staff):
    """Make page name for individual."""
    return f"{staff['family']}-{staff['personal']}.html"


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbfile", type=str, required=True, help="database file")
    parser.add_argument("--index", type=str, required=True, help="Index template file")
    parser.add_argument(
        "--pagedir", type=str, required=True, help="HTML page directory"
    )
    parser.add_argument("--params", type=str, required=True, help="parameter file")
    parser.add_argument("--seed", type=int, required=True, help="RNG seed")
    parser.add_argument("--staff", type=str, required=True, help="Staff template file")
    return parser.parse_args()


if __name__ == "__main__":
    main()
