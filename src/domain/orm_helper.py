from typing import Dict, Any


def orm_to_dict(orm) -> Dict[str, Any]:
    """
    :param orm: an SqlAlchemy ORM object
    :return: a dictionary with the declared field names as keys
    """
    return {column.name: str(getattr(orm, column.name)) for column in orm.__table__.columns}
