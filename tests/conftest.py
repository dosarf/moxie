PROPERTY_DB_SERVER = 'db_server'
PROPERTY_SCHEMA_CREATION = 'schema_creation'


def property_name_to_cli_option(property_name: str) -> str:
    return f'--{property_name.replace("_", "-")}'


# ... but on the command line, we want dashes instead
# of underscores (like '--hello-world').
CMD_LINE_OPTION_DB_SERVER = property_name_to_cli_option(PROPERTY_DB_SERVER)
CMD_LINE_OPTION_SCHEMA_CREATION = property_name_to_cli_option(PROPERTY_SCHEMA_CREATION)


def pytest_addoption(parser):
    parser.addoption(CMD_LINE_OPTION_SCHEMA_CREATION,
                     action='store',
                     default='orm',
                     help='How to create the schema (orm|migrate)')
    parser.addoption(CMD_LINE_OPTION_DB_SERVER,
                     action='store',
                     default='sqlite',
                     help='DB type (sqlite|postgres)')