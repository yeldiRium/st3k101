import click

from app import app
from framework import services
from model import db


@app.cli.command()
def initdb():
    """
    Initializes (creates) the database for SQLAlchemy.
    :return: None
    """
    click.echo("Creating the database defined in model...")
    db.create_all()
    click.echo("Done!")

# TODO: first time setup cli command

@app.cli.command()
def update_statistics():
    click.echo("Updating all statistics models...")
    services.update_all_statistics()
    click.echo("Done!")

