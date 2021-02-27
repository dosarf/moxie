# Running tests

```
$ PYTHONPATH=src:. pytest
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
$ PYTHONPATH=src pytest:. --schema-creation=migrate
```

## Testing on PostgreSQL

Unless specified otherwise, ORM query tests are run against
SQLite database (`--db-server=sqlite`).

To run against PostgreSQL, specify `--db-server=postgres`
on the CLI:

```
$ PYTHONPATH=src:. pytest --db-server=postgres
```

## Running all tests

To run all 2 x 2 = 4 combinations of possible tests:

```
$ ./test-all.sh
```

# Using CLI tool

Need tools `jo` and `jq` for easier JSON
handling on the CLI.

Default DB URL is `sqlite:///moxie.db`.

## Adding notes

Either specifying the JSON content as an argument, like

```
$ python src/main.py create --json-content='{"title":"First ever note"}' | jq
{
  "id": "1",
  "title": "First ever note"
}
```

or piping the JSON output from `jo` tool:

```
$ jo title="Second note, to follow" | python src/main.py create | jq
{
  "id": "2",
  "title": "Second note, to follow"
}
```

## Finding all notes

is as simple as

```
$ python src/main.py find-all | jq
[
  {
    "id": "1",
    "title": "First ever note"
  },
  {
    "id": "2",
    "title": "Second note, to follow"
  }
]
```

## Finding note by ID

goes with

```
$ python src/main.py find-by-id 2 | jq
{
  "id": "2",
  "title": "Second note, to follow"
}
```
