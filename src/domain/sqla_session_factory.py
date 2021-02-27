from contextlib import contextmanager

from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, Session


class SqlaSessionFactory:
    def __init__(self, engine: Engine):
        self.__engine = engine
        self.__create_session = sessionmaker(self.__engine)

    @contextmanager
    def __call__(self) -> Session:
        session = self.__create_session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as err:
            session.rollback()
            raise
        except Exception as err:
            session.rollback()
            raise
        finally:
            session.close()

    @property
    def engine(self) -> Engine:
        return self.__engine
