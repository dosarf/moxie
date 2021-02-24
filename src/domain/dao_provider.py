from sqlalchemy import create_engine

from domain.moxie_base import MoxieBase
from domain.moxie_note_dao import MoxieNoteDao
from domain.sqla_session_factory import SqlaSessionFactory


class DaoProvider:
    def __init__(self,
                 db_url: str,
                 create_schema: bool = False):
        self.__db_url = db_url

        self.__engine = create_engine(db_url)
        if create_schema:
            MoxieBase.metadata.create_all(self.__engine)

        self.__session_factory = SqlaSessionFactory(self.__engine)
        self.__moxie_note_dao = MoxieNoteDao(self.__session_factory)

    @property
    def moxie_note_dao(self) -> MoxieNoteDao:
        return  self.__moxie_note_dao
