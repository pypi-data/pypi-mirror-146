"""Top-level package for todo-cli-typer."""

__app_name__ = 'todo'
__version__ = '0.3.3'

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    ID_ERROR,
) = range(7)

ERRORS = {
    DIR_ERROR: 'config directory error',
    FILE_ERROR: 'config file error',
    DB_READ_ERROR: 'database read error',
    DB_WRITE_ERROR: 'database write error',
    ID_ERROR: 'to-do id error',
}
