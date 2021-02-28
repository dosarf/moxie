from typing import Dict, Any, List, Tuple

import pytest
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from domain.orm_moxie_note import OrmMoxieNote
from domain.moxie_note_dao import MoxieNoteDao, MoxieNote


@pytest.fixture()
def note_suite() -> List[Dict[str, Any]]:
    return [
        {'title': 'Awesome', 'content': 'Awesine content'},
        {'title': 'Another title', 'content': 'Another content'}
    ]


@pytest.fixture
def moxie_note_dao_with_suite(moxie_note_dao, note_suite) -> Tuple[MoxieNoteDao, List[MoxieNote]]:
    persisted_note_suite = [moxie_note_dao.create(**note_data) for note_data in note_suite]
    return moxie_note_dao, persisted_note_suite


def test_empty_persistence_has_no_notes(moxie_note_dao):
    assert len(moxie_note_dao.find_all()) == 0


def test_create_returns_created_note_with_id_assigned(moxie_note_dao):
    created_note = moxie_note_dao.create(title='Test title', content='Test content')

    assert created_note.title == 'Test title'
    assert created_note.content == 'Test content'
    assert created_note.id is not None


def test_note_title_is_mandatory_non_empty_and_non_blank(moxie_note_dao):
    note_count = len(moxie_note_dao.find_all())

    for title in [None, '', '   ']:
        with pytest.raises(IntegrityError, match='title'):
            moxie_note_dao.create(title=title, content='test content')

    assert len(moxie_note_dao.find_all()) == note_count


def test_note_title_r_n_t_backslash_are_preserved(moxie_note_dao):
    # If or when \r, \n or \t blanks are also prohibited, ordinary characters
    # like r, n, t or backslash (\) characters must be preserved.
    created_note = moxie_note_dao.create(title='rnt\\', content='test content')

    assert created_note.title == 'rnt\\'
    assert created_note.id is not None


def test_note_content_is_mandatory_non_empty_and_non_blank(moxie_note_dao):
    note_count = len(moxie_note_dao.find_all())

    for content in [None, '', '   ']:
        with pytest.raises(IntegrityError, match='content'):
            moxie_note_dao.create(title='test title', content=content)

    assert len(moxie_note_dao.find_all()) == note_count


def test_note_content_r_n_t_backslash_are_preserved(moxie_note_dao):
    # If or when \r, \n or \t blanks are also prohibited, ordinary characters
    # like r, n, t or backslash (\) characters must be preserved.
    created_note = moxie_note_dao.create(title='title', content='rnt\\')

    assert created_note.content == 'rnt\\'
    assert created_note.id is not None


def are_equivalent(first: OrmMoxieNote, second: OrmMoxieNote) -> bool:
    return \
        first.id == second.id \
        and first.title == second.title


def test_note_can_be_found_by_id(moxie_note_dao_with_suite):
    moxie_note_dao = moxie_note_dao_with_suite[0]
    first_persisted = moxie_note_dao_with_suite[1][0]

    found_note = moxie_note_dao.find_by_id(first_persisted.id)

    assert are_equivalent(found_note, first_persisted)


def test_find_all_orders_by_id(moxie_note_dao_with_suite):
    moxie_note_dao = moxie_note_dao_with_suite[0]

    notes = moxie_note_dao.find_all()

    note_ids = [note.id for note in notes]
    sorted_note_ids = list(note_ids)
    sorted_note_ids.sort()

    assert note_ids == sorted_note_ids
