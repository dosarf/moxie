from sqlalchemy import Column, Integer, String

from domain.moxie_base import MoxieBase


# TODO verify that comments end up as SQL comments
# https://github.com/sqlalchemy/sqlalchemy/issues/1546
# TODO verifu that these comments will be used by Postgraphile
# https://www.graphile.org/postgraphile/smart-comments/
class MoxieNote(MoxieBase):
    """
    @name MoxieNote
    @synopsis A note represents an atomic recipe, how-to, a 'gist'.
    """
    __tablename__ = 'note'

    id = Column(Integer, primary_key=True)

    # TODO in addition to being nullable, employ CHECK constraint, preferably via SqlAlchemy
    title = Column(String, nullable=False)
    """
    @name title
    @synopsis Short title of the note, either either in interrogative (How to do X?) or imperative (Do X)
    """
