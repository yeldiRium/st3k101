import click

from app import app
from model.SQLAlchemy import db


@app.cli.command()
def initdb():
    """
    Initializes (creates) the database for SQLAlchemy.
    :return: None
    """
    click.echo("Creating the database defined in model...")
    db.create_all()
    click.echo("Done!")
