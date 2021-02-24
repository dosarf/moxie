import pytest

from domain.dao_provider import DaoProvider
from domain.moxie_note_dao import MoxieNoteDao


@pytest.fixture()
def in_memory_db_url() -> str:
    return 'sqlite:///:memory:'


@pytest.fixture()
def dao_provider(in_memory_db_url: str) -> DaoProvider:
    return DaoProvider(db_url=in_memory_db_url,
                       create_schema=True)


@pytest.fixture()
def moxie_note_dao(dao_provider) -> MoxieNoteDao:
    return dao_provider.moxie_note_dao
