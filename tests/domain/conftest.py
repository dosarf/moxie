from enum import Enum
from pathlib import Path

import psycopg2
import pytest
from sqlalchemy.engine import Engine, create_engine

from domain.dao_provider import DaoProvider
from domain.moxie_base import MoxieBase
from domain.moxie_note_dao import MoxieNoteDao

# Property names, as obtained from request.config.getoption
# are to have underscores (like 'hello_world') ...
from migration_helper import get_repository, version_and_apply_schema_scripts
from tests.conftest import PROPERTY_SCHEMA_CREATION, PROPERTY_DB_SERVER


class SchemaCreation(Enum):
    ORM = 0
    MIGRATE = 1


@pytest.fixture(scope='session')
def schema_creation(request) -> SchemaCreation:
    """
    The value translated from CLI option CMD_LINE_OPTION_SCHEMA_CREATION
    to :class:`SchemaCreation`
    """
    option = request.config.getoption(PROPERTY_SCHEMA_CREATION)
    return SchemaCreation[option.upper()]


class DbServer(Enum):
    SQLITE = 0
    POSTGRES = 1


@pytest.fixture(scope='session')
def db_server(request) -> DbServer:
    """
    The value translated from CLI option CMD_LINE_OPTION_DB_SERVER
    to :class:`DbServer`
    """
    option = request.config.getoption(PROPERTY_DB_SERVER)
    return DbServer[option.upper()]


@pytest.fixture(scope='session')
def docker_compose_file(pytestconfig) -> str:
    path = Path(str(pytestconfig.rootdir)) / 'tests' / 'domain' / 'docker-compose.yml'
    return str(path)


def is_responsive(db_url: str) -> bool:
    """
    :param db_url:
    :return: True if it could create a PostgreSQL connection to
        specified db_url
    """
    try:
        connection = psycopg2.connect(db_url)
        connection.close()
        return True
    except psycopg2.OperationalError:
        return False


@pytest.fixture(scope='session')
def postgres(docker_ip, docker_services) -> str:
    """
    Kicks in the services defined in the docker-compose file.

    :return: the DB URL to connect to the postgresql instance running
        in the docker container
    """

    port = docker_services.port_for('postgres', 5432)

    # To be consistent with tests/domain/docker-compose.yml.
    # TODO Consider doing:
    # - require fixture docker_compose.yml
    # - read its YAML (user, password, DB name),
    # - and then construct this URL out of its contents
    db_url = f'postgres://postgres:pwd@{docker_ip}:{port}/moxie-test'

    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(db_url)
    )
    return db_url


@pytest.fixture(scope='session')
def engine(schema_creation, db_server, request, tmp_path_factory) -> Engine:
    """
    An SqlAlchemy Engine instance connected to the DB specified by
    fixtures schema_creation, db_server (translated from CLI args).

    In PostgreSQL mode (db_server is DbServer.POSTGRES) it dynamically
    requires fixture 'postgres', which will bring up a docker container
    to run a temporary PostgreSQL installation to test within.
    """
    db_url: str = None

    if db_server == DbServer.SQLITE:
        if SchemaCreation.ORM == schema_creation:
            db_url = 'sqlite:///:memory:'
        else:
            tmp_db_path = tmp_path_factory.mktemp('moxie-test') / 'moxie-test.db'
            db_url = f'sqlite:///{str(tmp_db_path)}'
    else:  # DbServer.POSTGRES
        db_url = request.getfixturevalue('postgres')

    return create_engine(db_url)


@pytest.fixture(scope='session')
def dao_provider(engine, schema_creation) -> DaoProvider:
    """
    DaoProvider instance, with a schema initialized,
    providing DAO service instances from.
    """
    if SchemaCreation.MIGRATE == schema_creation:
        version_and_apply_schema_scripts(str(engine.url),
                                         get_repository())

    create_schema: bool = SchemaCreation.ORM == schema_creation
    obj = DaoProvider(engine=engine, create_schema=create_schema)

    yield obj

    obj.close()


@pytest.fixture(scope='session')
def moxie_note_dao(dao_provider) -> MoxieNoteDao:
    """
    The instance of service :class:`~domain.moxie_note_dao.MoxieNoteDao`
    provided by (fixture) dao_provider.
    """
    return dao_provider.moxie_note_dao
