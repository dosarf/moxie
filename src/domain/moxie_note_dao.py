from dataclasses import dataclass, field
from typing import Optional, List

from domain.orm_moxie_note import OrmMoxieNote
from domain.sqla_session_factory import SqlaSessionFactory


@dataclass(frozen=True, repr=True, eq=True)
class MoxieNote:
    """
    Represents a (moxie) note
    """
    id: int = field(repr=True, compare=True)
    title: str = field(repr=True, compare=False)


class MoxieNoteDao:
    """
    Service giving access to moxie notes.
    """
    def __init__(self,
                 session_factory: SqlaSessionFactory):
        self.__create_session = session_factory

    def find_by_id(self, id: int) -> Optional[MoxieNote]:
        with self.__create_session() as session:
            orm = session.query(OrmMoxieNote).filter(OrmMoxieNote.id == id).one_or_none()
            return MoxieNoteDao.orm_to_api(orm)
        # TODO omitted exception translation now

    def find_all(self) -> List[MoxieNote]:
        with self.__create_session() as session:
            return [MoxieNoteDao.orm_to_api(orm)
                    for orm in session.query(OrmMoxieNote).order_by(OrmMoxieNote.id)
                    ]
        # TODO omitted exception translation now

    def create(self,
               title: str) -> MoxieNote:
        orm = OrmMoxieNote(title=title)
        with self.__create_session() as session:
            session.add(orm)
            session.flush()
            return MoxieNoteDao.orm_to_api(orm)
        # TODO omitted exception translation now


    @staticmethod
    def orm_to_api(orm: Optional[OrmMoxieNote]) -> Optional['MoxieNote']:
        if orm is not None:
            return MoxieNote(id=orm.id,
                             title=orm.title)
        return None
