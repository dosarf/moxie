import json
import os
import pathlib
import sys

import click
import migrate
import migrate.versioning.api
from migrate.versioning.repository import Repository
from sqlalchemy import create_engine

from domain.dao_provider import DaoProvider
from domain.orm_helper import orm_to_dict


@click.group()
def cli():
    """Entry point for multiple click commands
    See https://click.palletsprojects.com/en/7.x/quickstart/#nesting-commands
    """


DEFAULT_DB_URL: str ='sqlite:///moxie.db'
"""
DB URL to use by default
"""


REPOSITORY_FOLDER: str = 'moxie_schema_repository'
"""
The folder in which the version controlled schema migration scripts
are stored, relative to the root folder of this project.
"""


@cli.command()
@click.option('--db-url', default=DEFAULT_DB_URL, help='URL of DB to use')
def upgrade_schema(db_url: str):
    """
    Upgrades the schema of a DB, using the migrator API.
    """
    repository_path = pathlib.Path(os.getcwd(), REPOSITORY_FOLDER)
    if not repository_path.exists() or not repository_path.is_dir():
        click.echo(f'Cannot find {REPOSITORY_FOLDER}')
        sys.exit(1)

    repository = Repository(str(repository_path))

    migrate.versioning.api.version_control(url=db_url, repository=repository)
    migrate.versioning.api.upgrade(url=db_url, repository=repository)

    with DaoProvider(db_url) as dao_provider:
        click.echo(f'Schema upgraded for {dao_provider.db_url}')


@cli.command()
@click.option('--db-url', default=DEFAULT_DB_URL, help='URL of DB to use')
def create_schema(db_url: str):
    """
    Creates the entire (current) schema of a DB, without using the migrator API.
    DB schema created this way cannot be migrated with 'upgrade_schema'.
    """
    with DaoProvider(db_url, create_schema=True) as dao_provider:
        click.echo(f'Schema created for {dao_provider.db_url}')


@cli.command()
@click.option('--db-url', default=DEFAULT_DB_URL, help='URL of DB to use')
def find_all(db_url: str):
    """
    Finds all (moxie) notes.
    """
    dao_provider = DaoProvider(db_url, create_schema=False)
    notes = dao_provider.moxie_note_dao.find_all()
    json_notes = json.dumps([orm_to_dict(note) for note in notes])
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
    with DaoProvider(db_url) as dao_provider:
        note = dao_provider.moxie_note_dao.find_by_id(id)
        if note:
            click.echo(json.dumps(orm_to_dict(note)))
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

    with DaoProvider(db_url) as dao_provider:
        note = dao_provider.moxie_note_dao.create(**content)
        click.echo(json.dumps(orm_to_dict(note)))


if __name__ == '__main__':
    cli()
