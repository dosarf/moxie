from migrate import CheckConstraint
from sqlalchemy import MetaData, Table, Column, String


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata

    # this script has been tested only on PostgreSQL
    # in particular, SQLite does not implement all the necessary
    # ALTER TABLE ... constructs from standard SQL
    if migrate_engine.name != 'postgresql':
        return

    meta = MetaData(bind=migrate_engine)
    note = Table('note', meta, autoload=True)

    # Here https://sqlalchemy-migrate.readthedocs.io/en/latest/changeset.html#column-create
    # shows a way to populate a column, at its creation, with a default
    # value, something like this could work:
    # content = Column('content', String, CheckConstraint(...), nullable=False, default='TODO content')
    # content.create(note, populate_default=True)
    #
    # Except now we want to try how to populate a new column with
    # *calculated* values, from DB itself.
    # no constraints yet
    # comments given here don't end up in DB (PostgreSQL) need different migration script for it
    content = Column('content', String)
    content.create(note)

    # populate new column
    populating_statement = note.update().values(content='TODO content: ' + note.c.title)

    with migrate_engine.connect() as connection:
        connection.execute(populating_statement)

    # add constraints to populated column content (not-null, CHECK)
    content.alter(nullable=False)

    check_constraint = CheckConstraint(
        sqltext=r"length(trim(content, ' ')) > 0",
        name='note_non_blank_content',
        columns=[content])
    check_constraint.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.

    # upgrade was specific to PostgreSQL and so it
    # downgrade (see above)
    if migrate_engine.name != 'postgresql':
        return

    meta = MetaData(bind=migrate_engine)
    note = Table('note', meta, autoload=True)
    note.c.content.drop()
