"""Query the plate database."""

import click

from query_direct import query_direct

TABLES = click.Choice(["staff", "exp", "plate"])
METHODS = {
    "direct": query_direct,
}
FUNCS = click.Choice(METHODS.keys())


@click.group()
def cli():
    pass


@cli.command()
@click.option("--how", type=FUNCS, help="how to execute query")
@click.option("--which", type=TABLES, help="count")
@click.argument("dbfile")
def count(how, which, dbfile):
    print(METHODS[how]("count", which, dbfile))


@cli.command()
@click.option("--how", type=FUNCS, help="how to execute query")
@click.option("--which", type=TABLES, help="list")
@click.argument("dbfile")
def ls(how, which, dbfile):
    print(METHODS[how]("ls", which, dbfile))


if __name__ == "__main__":
    cli()
