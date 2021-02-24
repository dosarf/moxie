#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(repository='moxie_schema_repository', url='postgres://postgres:pwd@localhost/moxie', debug='False')
