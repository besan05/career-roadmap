"""Creator scripts as Flask CLI commands (architecture.md).

Only init-db so far. The creator scripts arrive in ticket 03.
"""

import click
from flask import current_app
from flask.cli import with_appcontext

from .data.db import init_db


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Create every table from schema.sql in the database at DATABASE_PATH."""
    database_path = current_app.config["DATABASE_PATH"]
    if not init_db():
        # Refusing, rather than dropping tables, means a second run can
        # never wipe real data on production.
        raise click.ClickException(
            f"The database at {database_path} already has tables, so "
            "nothing was changed. To start over on your laptop only, "
            "delete that file and run flask init-db again."
        )
    click.echo(f"Database created at {database_path}")
