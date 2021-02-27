import json
import sys

import click

from domain.dao_provider import DaoProvider
from migration_helper import version_and_apply_schema_scripts, get_repository


@click.group()
def cli():
    """Entry point for multiple click commands
    See https://click.palletsprojects.com/en/7.x/quickstart/#nesting-commands
    """


DEFAULT_DB_URL: str ='sqlite:///moxie.db'
"""
DB URL to use by default
"""


@cli.command()
@click.option('--db-url', default=DEFAULT_DB_URL, help='URL of DB to use')
def upgrade_schema(db_url: str):
    """
    Upgrades the schema of a DB, using the migrator API.
    """
    version_and_apply_schema_scripts(db_url,
                                     get_repository())

    with DaoProvider.from_db_url(db_url) as dao_provider:
        click.echo(f'Schema upgraded for {dao_provider.db_url}')


@cli.command()
@click.option('--db-url', default=DEFAULT_DB_URL, help='URL of DB to use')
def create_schema(db_url: str):
    """
    Creates the entire (current) schema of a DB, without using the migrator API.
    DB schema created this way cannot be migrated with 'upgrade_schema'.
    """
    with DaoProvider.from_db_url(db_url, create_schema=True) as dao_provider:
        click.echo(f'Schema created for {dao_provider.db_url}')


@cli.command()
@click.option('--db-url', default=DEFAULT_DB_URL, help='URL of DB to use')
def find_all(db_url: str):
    """
    Finds all (moxie) notes.
    """
    dao_provider = DaoProvider.from_db_url(db_url, create_schema=False)
    notes = dao_provider.moxie_note_dao.find_all()
    json_notes = json.dumps([note.__dict__ for note in notes])
    click.echo(json_notes)


@cli.command()
@click.option('--db-url', default=DEFAULT_DB_URL, help='URL of DB to use')
@click.argument('id')
def find_by_id(
        id: int,
        db_url: str):
    """
    Finds a (moxie) note by its ID.
    """
    with DaoProvider.from_db_url(db_url) as dao_provider:
        note = dao_provider.moxie_note_dao.find_by_id(id)
        if note:
            click.echo(json.dumps(note.__dict__))
        else:
            sys.exit(1)


@cli.command()
@click.option('--json-content', default=None, help='JSON content of moxie note to persist')
@click.option('--db-url', default=DEFAULT_DB_URL, help='URL of DB to use')
def create(
        json_content: str,
        db_url: str):
    """
    Creates a (moxie) note, based on a JSON content (for now, only title).
    """
    if json_content is None:
        with click.get_text_stream('stdin') as stdin:
            json_content = stdin.read()

    content = json.loads(json_content)

    with DaoProvider.from_db_url(db_url) as dao_provider:
        note = dao_provider.moxie_note_dao.create(**content)
        click.echo(json.dumps(note.__dict__))


if __name__ == '__main__':
    cli()
