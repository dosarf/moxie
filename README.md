# Running tests

```
$ PYTHONPATH=src:. pytest tests/
```

or from PyCharm.

## Testing migrated schema

By default, the unit tests for ORM queries (SqlAlchemy)
are tested on a schema that's generated out of the ORM
class definitions (`--schema-creation=orm`).

> Production code using declarative ORM classes know only
> about the (latest) schema as defined by those ORM classes.
> In other words, production code knows only about
> the ORM-defined schema.
>
> On the other hand, real DBs have _migrated_ schemas, which
> may or may not be identical to what production code thinks
> it has to work with.
>
> Ideally, there should tests verifying that the latest schema
> defined by declarative ORM classes is identical to a
> migrated schema (TODO).
> 
> In the absence of such schema equivalence verification,
> the next best thing is to test ORM queries against both
> type of schema - they should both pass.

To run the unit tests for the ORM queries, use the custom CLI
option `--schema-creation=migrate`:

```
$ PYTHONPATH=src pytest:. --schema-creation=migrate tests/
```

## Testing on PostgreSQL

Unless specified otherwise, ORM query tests are run against
SQLite database (`--db-server=sqlite`).

To run against PostgreSQL, specify `--db-server=postgres`
on the CLI:

```
$ PYTHONPATH=src:. pytest --db-server=postgres tests/
```

## Running all tests

To run all 2 x 2 = 4 combinations of possible tests:

```
$ ./test-all.sh
```

# Using CLI tool

Need tools `jo` and `jq` for easier JSON handling on the CLI.

Default DB URL is `sqlite:///moxie.db`.

## Creating DB

For instance, for a custom DB URL `bla.db`:
```
$ python src/main.py upgrade-schema --db-url=sqlite:///bla.db
Schema upgraded for sqlite:///bla.db
```

> For a PostgreSQL connection, use `postgresql://user:password@host:port/moxie`,
> provided the database to use is called `moxie`.

## Adding notes

Either specifying the JSON content as an argument, like

```
$ python src/main.py create --json-content='{"title":"First ever note","content":"... and its content."}' | jq
{
  "id": 1,
  "title": "First ever note",
  "content": "... and its content."
}
```

or piping the JSON output from `jo` tool:

```
$ jo title="Second note, to follow" content="it also has some contents" | python src/main.py create | jq
{
  "id": 2,
  "title": "Second note, to follow",
  "content": "it also has some contents"
}
```

## Finding all notes

is as simple as

```
$ python src/main.py find-all | jq
[
  {
    "id": 1,
    "title": "First ever note",
    "content": "... and its content."
  },
  {
    "id": 2,
    "title": "Second note, to follow",
    "content": "it also has some contents"
  }
]
```

## Finding note by ID

goes with

```
$ python src/main.py find-by-id 2 | jq
{
  "id": 2,
  "title": "Second note, to follow",
  "content": "it also has some contents"
}
```

# Using CLI tool with PostgreSQL

## Start a PostgreSQL service in a docker container

In order to test migration scripts, it's best to use a folder
in the host filesystem for the PostgreSQL data folder (`PGDATA`),
so that even if containers are stopped / destoyed, the data
remains.

Create `pgdata/` by:

```
$ mkdir pgdata
```

> That folder is already in `.gitignore`.

Then start a PostgreSQL service in docker:

```
$ docker run --name moxie-psql -p 5432:5432 -e POSTGRES_PASSWORD=pwd -e PGDATA=/var/lib/postgresql/data/pgdata -e POSTGRES_DB=moxie -v $(pwd)/pgdata:/var/lib/postgresql/data/pgdata -d postgres:latest
```

Verify the container, the contents of `pgdata/` and the database
`moxie` created on startup, entering `pwd` for password when prompted:

```
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
ffa92eebe209        postgres:latest     "docker-entrypoint.s…"   7 minutes ago       Up 7 minutes        0.0.0.0:5432->5432/tcp   moxie-psql
$ sudo ls pgdata/
base	      pg_hba.conf    pg_notify	   pg_stat	pg_twophase  postgresql.auto.conf
global	      pg_ident.conf  pg_replslot   pg_stat_tmp	PG_VERSION   postgresql.conf
pg_commit_ts  pg_logical     pg_serial	   pg_subtrans	pg_wal	     postmaster.opts
pg_dynshmem   pg_multixact   pg_snapshots  pg_tblspc	pg_xact      postmaster.pid
$ psql -U postgres -d moxie -h localhost -c "\d"
Password for user postgres: 
Did not find any relations.
```

So DB `moxie` exists but it's empty so far'.

> The DB URL to is is `postgres://postgres:pwd@localhost/moxie`

## Version + init schema

The CLI tool `src/main.py` also supports taking a DB under schema
version control and upgrading its schema:

```
$ python src/main.py upgrade-schema --db-url=postgres://postgres:pwd@localhost/moxie
Schema upgraded for postgres://postgres:***@localhost/moxie
```

Verify the successful schema versioning and initialization by:

```
$ psql -U postgres -d moxie -h localhost -c "\d"
Password for user postgres: 
               List of relations
 Schema |      Name       |   Type   |  Owner   
--------+-----------------+----------+----------
 public | migrate_version | table    | postgres
 public | note            | table    | postgres
 public | note_id_seq     | sequence | postgres
(3 rows)
$ psql -U postgres -d moxie -h localhost -c "\d note"
Password for user postgres: 
                                 Table "public.note"
 Column |       Type        | Collation | Nullable |             Default              
--------+-------------------+-----------+----------+----------------------------------
 id     | integer           |           | not null | nextval('note_id_seq'::regclass)
 title  | character varying |           | not null | 
 ...
Indexes:
    "note_pkey" PRIMARY KEY, btree (id)
Check constraints:
    "note_non_blank_title" CHECK (length(btrim(title::text, ' '::text)) > 0)
...
```

- table `migrate_version` is the internal table used by
  SqlAlchemy Migrate to track version of the DB schema

- table `note` belongs to our application schema along with
  its sequence `note_id_seq` to create a sequence of note
  IDs
  
  - notice how column `note.title` is not only non-nullable
    but has a `CHECK` constraint that was specified by
    our migration scripts

## Verify schema comments

We have comments (both in the declarative ORM types as well as in the migration
scripts) that we want to end up in the PostgreSQL schema.

> Based on https://github.com/sqlalchemy/sqlalchemy/issues/1546,
> it should work.

Let's check it for both tables and columns:

```
$ psql -U postgres -d moxie -h localhost -x -f query-psql-comments.psql 
Password for user postgres: 
-[ RECORD 1 ]------------------------------------------------------------------------------------------------------
schemaname  | public
tablename   | note
type        | TABLE
columnname  | 
description | @name MoxieNote                                                                                      +
            | @synopsis A note represents an atomic recipe, how-to, a gist.
relid       | 16395
objsubid    | 0
-[ RECORD 2 ]------------------------------------------------------------------------------------------------------
schemaname  | public
tablename   | note
type        | COLUMN
columnname  | title
description | @name title                                                                                          +
            | @synopsis Short title of the note, either either in interrogative (How to do X?) or imperative (Do X)
relid       | 16395
objsubid    | 2
...
```
