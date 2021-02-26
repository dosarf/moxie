from enum import Enum

import pytest

from domain.dao_provider import DaoProvider
from domain.moxie_note_dao import MoxieNoteDao

# Property names, as obtained from request.config.getoption
# are to have underscores (like 'hello_world') ...
from migration_helper import get_repository, version_and_apply_schema_scripts

PROPERTY_SCHEMA_CREATION = 'schema_creation'


def property_name_to_cli_option(property_name: str) -> str:
    return f'--{property_name.replace("_", "-")}'


# ... but on the command line, we want dashes instead
# of underscores (like '--hello-world').
CMD_LINE_OPTION_SCHEMA_CREATION = property_name_to_cli_option(PROPERTY_SCHEMA_CREATION)


def pytest_addoption(parser):
    parser.addoption(CMD_LINE_OPTION_SCHEMA_CREATION,
                     action='store',
                     default='orm',
                     help='How to create the schema (orm|migrate)')


class SchemaCreation(Enum):
    ORM = 0
    MIGRATE = 1


@pytest.fixture()
def schema_creation(request) -> SchemaCreation:
    """
    The value translated from CLI option CMD_LINE_OPTION_SCHEMA_CREATION
    to :class:`SchemaCreation`
    """
    option = request.config.getoption("schema_creation")
    return SchemaCreation[option.upper()]


@pytest.fixture()
def db_url(schema_creation, tmp_path) -> str:
    """
    The DB URL to use, depending on schema_creation mode.
    """
    if SchemaCreation.ORM == schema_creation:
        return 'sqlite:///:memory:'
    else:
        tmp_db_path = tmp_path / 'temp.db'
        return f'sqlite:///{str(tmp_db_path)}'


@pytest.fixture()
def dao_provider(db_url: str, schema_creation) -> DaoProvider:
    """
    An instance of the :class:~domain.dao_provider.DaoProvider`,
    initialized either with the latest-and-greatest (snapshot) of
    SqlAlchemy schema definitions in use, or, applying
    SqlAlchemy Migration API and all of the migration script repository.

    The ORM tests must pass for both kind of schema creation policy.
    """
    if SchemaCreation.ORM == schema_creation:
        return DaoProvider(db_url=db_url,
                           create_schema=True)
    else:
        version_and_apply_schema_scripts(db_url,
                                         get_repository())
        return DaoProvider(db_url=db_url,
                           create_schema=False)


@pytest.fixture()
def moxie_note_dao(dao_provider) -> MoxieNoteDao:
    """
    The instance of service :class:`~domain.moxie_note_dao.MoxieNoteDao`
    provided by (fixture) dao_provider.
    """
    return dao_provider.moxie_note_dao
