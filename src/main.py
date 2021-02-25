import json
import sys

import click

from domain.dao_provider import DaoProvider
from domain.orm_helper import orm_to_dict


@click.group()
def cli():
    """Entry point for multiple click commands
    See https://click.palletsprojects.com/en/7.x/quickstart/#nesting-commands
    """


DEFAULT_DB_URL: str ='sqlite:///temp-moxie.db'
"""
DB URL to use by default
"""

CREATE_SCHEMA: bool = True


@cli.command()
@click.option('--db-url', default=DEFAULT_DB_URL, help='URL of DB to use')
def find_all(db_url: str):
    dao_provider = DaoProvider(db_url, create_schema=CREATE_SCHEMA)
    # click.echo(f'URL: {dao_provider.db_url}')
    notes = dao_provider.moxie_note_dao.find_all()
    json_notes = json.dumps([orm_to_dict(note) for note in notes])
    click.echo(json_notes)


@cli.command()
@click.option('--db-url', default=DEFAULT_DB_URL, help='URL of DB to use')
@click.argument('id')
def find_by_id(
        id: int,
        db_url: str):
    dao_provider = DaoProvider(db_url, create_schema=CREATE_SCHEMA)
    # click.echo(f'URL: {dao_provider.db_url}')
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
    dao_provider = DaoProvider(db_url, create_schema=CREATE_SCHEMA)
    # click.echo(f'URL: {dao_provider.db_url}')
    if json_content is None:
        with click.get_text_stream('stdin') as stdin:
            json_content = stdin.read()
    content = json.loads(json_content)
    note = dao_provider.moxie_note_dao.create(**content)
    click.echo(json.dumps(orm_to_dict(note)))


if __name__ == '__main__':
    cli()
