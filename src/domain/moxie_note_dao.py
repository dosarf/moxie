from typing import Optional, List

from domain.moxie_note import MoxieNote
from domain.sqla_session_factory import SqlaSessionFactory


class MoxieNoteDao:
    def __init__(self,
                 session_factory: SqlaSessionFactory):
        self.__create_session = session_factory

    def find_by_id(self, id: int) -> Optional[MoxieNote]:
        with self.__create_session() as session:
            return session.query(MoxieNote).filter(MoxieNote.id == id).one_or_none()
        # TODO omitted exception translation now

    def find_all(self) -> List[MoxieNote]:
        with self.__create_session() as session:
            return list(session.query(MoxieNote).order_by(MoxieNote.id))
        # TODO omitted exception translation now

    def create(self,
               title: str) -> MoxieNote:
        note = MoxieNote(title=title)
        with self.__create_session() as session:
            session.add(note)
        # TODO omitted exception translation now
        return note
