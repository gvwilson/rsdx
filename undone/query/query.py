"""Query the plate database."""

import click

from query_direct import query_direct
from query_pony import query_pony


TABLES = click.Choice(["staff", "exp", "plate"])
METHODS = {
    "direct": query_direct,
    "pony": query_pony,
}
FUNCS = click.Choice(METHODS.keys())


@click.group()
def cli():
    """Command-line group."""


@cli.command()
@click.option("--how", type=FUNCS, help="how to execute query")
@click.option("--which", type=TABLES, help="count")
@click.argument("dbfile")
def count(how, which, dbfile):
    """Count entries in database."""
    click.echo(METHODS[how](dbfile, "count", which))


@cli.command()
@click.option("--how", type=FUNCS, help="how to execute query")
@click.argument("dbfile")
def invalidated(how, dbfile):
    """Display information about invalidated plates."""
    click.echo(METHODS[how](dbfile, "invalidated"))


@cli.command()
@click.option("--how", type=FUNCS, help="how to execute query")
@click.option("--which", type=TABLES, help="list")
@click.argument("dbfile")
def ls(how, which, dbfile):
    """List entries in database."""
    click.echo(METHODS[how](dbfile, "ls", which))


if __name__ == "__main__":
    cli()
