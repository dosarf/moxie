# Running tests

```
$ PYTHONPATH=src pytest
```

or from PyCharm.

## Testing migrated schema

By default, the unit tests for ORM queries (SqlAlchemy)
are tested on a schema that's generated out of the ORM
class definitions.

On the other hand, real DBs have migrated schemas. To
run the unit tests for the ORM queries, use the custom CLI
option `--schema-creation=migrate`:

```
$ PYTHONPATH=src pytest --schema-creation=migrate
```

# Running CLI tool

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
