import click

from app import app
from auth.roles import Role
from framework import importer
from framework.internationalization.babel_languages import BabelLanguage
from model import db
from model.models.DataClient import DataClient
from framework.flask import setup_app_context


@app.cli.command()
def initdb():
    """
    Initializes (creates) the database for SQLAlchemy.
    :return: None
    """
    click.echo("Creating the database defined in model...")
    db.create_all()
    click.echo("Done!")


@app.cli.command()
@click.option(
    '--email',
    type=str,
    prompt='Email Address',
    help='The DataClient\'s email address.'
)
@click.option(
    '--role',
    type=click.Choice([role.name for role in Role]),
    default=Role.User.name,
    help='The initial role the DataClient will have.'
)
@click.option(
    '--language',
    type=click.Choice([lang.name for lang in BabelLanguage]),
    default=app.config['BABEL_DEFAULT_LOCALE'],
    help='The DataClient\'s language.'
)
@click.argument(
    'click_stdin',
    type=click.File('r'),
    required=False
)
def register(email, role, language, click_stdin):
    click.echo('Creating new {} <{}> ...'.format(role, email))

    setup_app_context(app)

    dataclient = DataClient(email=email, verified=True, language=language)
    dataclient.add_role(next((r for r in Role if r.name == role)))

    password = None
    if click_stdin:  # try to read from stdin first (use this for piping passwords to this)
        password = click_stdin.read(512)
    if not password:
        password = click.prompt('Please enter a password for the new DataClient', type=str)
    if not password:
        db.session.rollback()
        click.echo('Empty password provided, changes were rolled back.')
        return
    dataclient.password = password

    db.session.add(dataclient)
    db.session.commit()
    click.echo('Done!')


@app.cli.command()
@click.option(
    '--owner',
    type=str,
    prompt='Owner\'s email address',
    help='The email address of the DataClient who will own the imported questionnaires.'
)
@click.argument(
    'file',
    type=click.File('r')
)
def import_questionnaires(owner, file):
    dataclient = DataClient.query.filter_by(email=owner).first()
    if not dataclient:
        click.echo('No DataClient with this email exists, aborting.')
        return
    setup_app_context(app, user=dataclient)
    contents = file.read()
    importer.import_questionnaires(contents)
    db.session.commit()


@app.cli.command()
@click.pass_context
def setup(ctx):
    ctx.invoke(initdb)
    ctx.invoke(register, role=Role.Root.name)
    # TODO: parse & insert first templates
