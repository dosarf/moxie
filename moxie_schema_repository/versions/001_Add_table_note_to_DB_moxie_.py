from sqlalchemy import *
from migrate import *

meta = MetaData()

"""
Corresponds directly to the first version of
:class:`~domain.moxie_note.MoxieNote`
"""
note = Table(
    'note',
    meta,
    Column(
        'id',
        Integer,
        primary_key=True),
    Column(
        'title',
        String,
        CheckConstraint(r"length(trim(title, ' ')) > 0", name='note_non_blank_title'),
        nullable=False,
        comment='@name title\n@synopsis Short title of the note, either either in interrogative (How to do X?) or imperative (Do X)'),
    comment='@name MoxieNote\n@synopsis A note represents an atomic recipe, how-to, a gist.'
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    note.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    note.drop()
