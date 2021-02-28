#! /bin/bash

for db_server in sqlite postgres
do
  # echo db_server
  for schema_creation in orm migrate
  do
    # echo $schema_creation
    echo PYTHONPATH=src:. pytest --db-server=$db_server --schema-creation=$schema_creation tests
    PYTHONPATH=src:. pytest --db-server=$db_server --schema-creation=$schema_creation tests
    [ $? -eq 0 ] || exit 1
  done
done

echo ALL combinations succeeded
echo DONE
