"""Opening the database and creating its tables.

All database access lives in app/data (rules.md section 3), so the
init-db command calls this module instead of running SQL itself.
"""

import sqlite3
from pathlib import Path

from flask import current_app

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schema.sql"


def get_connection():
    connection = sqlite3.connect(current_app.config["DATABASE_PATH"])
    connection.row_factory = sqlite3.Row
    # SQLite only enforces the foreign keys in schema.sql when this is
    # switched on, and it has to be switched on for every connection.
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    """Create every table from schema.sql.

    Returns False and changes nothing if the database already has tables.
    """
    connection = get_connection()
    try:
        table_count = connection.execute(
            "SELECT count(*) FROM sqlite_master WHERE type = 'table'"
        ).fetchone()[0]
        if table_count:
            return False

        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        # One transaction, so a broken schema never leaves some tables
        # created and others missing (rules.md section 8: nothing half-saved).
        connection.executescript("BEGIN;\n" + schema + "\nCOMMIT;")
        return True
    except sqlite3.Error:
        connection.rollback()
        raise
    finally:
        connection.close()
