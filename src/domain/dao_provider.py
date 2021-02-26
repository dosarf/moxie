from contextlib import AbstractContextManager

from sqlalchemy import create_engine

from domain.moxie_base import MoxieBase
from domain.moxie_note_dao import MoxieNoteDao
from domain.sqla_session_factory import SqlaSessionFactory


class DaoProvider(AbstractContextManager):
    """
    Entry point class for accessing all DAO services
    """
    def __init__(self,
                 db_url: str,
                 create_schema: bool = False):
        """
        :param db_url: DB URL to open
        :param create_schema: meant for (unit) tests, to create the entire
            schema of the current version (no schema migration)
        """
        self.__db_url = db_url

        self.__engine = create_engine(db_url)
        if create_schema:
            MoxieBase.metadata.create_all(self.__engine)

        self.__session_factory = SqlaSessionFactory(self.__engine)
        self.__moxie_note_dao = MoxieNoteDao(self.__session_factory)

    @property
    def moxie_note_dao(self) -> MoxieNoteDao:
        """
        :return: The DAO service to access moxie notes
        """
        return self.__moxie_note_dao

    @property
    def db_url(self) -> str:
        """
        :return: A DB URL safe for logging purposes
        """
        return repr(self.__engine.url)

    def close(self) -> None:
        """
        Closes all DB resources associated.
        """
        self.__engine.dispose()
        self.__engine = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
