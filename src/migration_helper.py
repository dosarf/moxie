import os
import pathlib

import migrate.versioning.api
from migrate.versioning.repository import Repository

REPOSITORY_FOLDER: str = 'moxie_schema_repository'
"""
The folder in which the version controlled schema migration scripts
are stored, relative to the root folder of this project.
"""


def get_repository() -> Repository:
    """
    Repository migration script definitions are to be at the relative
    path REPOSITORY_FOLDER.

    :return: A newly constructed :class:`~migrate.versioning.repository.Repository`
        instance, giving access to schema migration scripts of this project.
    """
    repository_path = pathlib.Path(os.getcwd(), REPOSITORY_FOLDER)
    if not repository_path.exists() or not repository_path.is_dir():
        raise ValueError(f'Cannot locate migration repository at {repository_path}')

    return Repository(str(repository_path))


def version_and_apply_schema_scripts(db_url: str,
                                     repository: Repository):
    """
    Switches schema version control on in given DB, and applies all schema migration
    scripts to the same DB.
    :param db_url:
    :param repository:
    """
    migrate.versioning.api.version_control(url=db_url, repository=repository)
    migrate.versioning.api.upgrade(url=db_url, repository=repository)
