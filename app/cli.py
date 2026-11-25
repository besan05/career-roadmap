"""Creator scripts as Flask CLI commands (architecture.md, D26, D61).

Each command checks its input before writing anything. A password or
code is generated only after every check has passed, and printed once,
only after it has been saved. It is never logged.
"""

import secrets
import sqlite3
from contextlib import contextmanager

import click
from flask import current_app
from flask.cli import with_appcontext

from .data import invites, users
from .data.db import init_db

# R1: passwords have at least 8 characters. 12 random bytes give 16.
PASSWORD_BYTES = 12


def register_commands(app):
    for command in (
        init_db_command,
        create_creator_command,
        create_invite_command,
        create_demo_command,
    ):
        app.cli.add_command(command)


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


@click.command("create-creator")
@click.argument("email")
@with_appcontext
def create_creator_command(email):
    """Create the creator account and print its password once."""
    email = _valid_email_or_refuse(email)
    with _database_errors():
        # D49: there is one creator. Checked here, not in schema.sql.
        if users.creator_exists():
            raise _refusal("A creator account already exists.")
        _refuse_if_email_taken(email)

        password = secrets.token_urlsafe(PASSWORD_BYTES)
        # The creator never ticks "I agree", so consented_at stays
        # empty (R1b, data-model.md).
        users.create_user(email, password, role=users.CREATOR)
    _print_password("Creator account", email, password)


@click.command("create-invite")
@with_appcontext
def create_invite_command():
    """Create a single-use invite code and print it once."""
    with _database_errors():
        code = invites.generate_invite_code()
        invites.save_invite_code(code)
    click.echo(f"Invite code created in {_database_path()}.")
    click.echo(f"Code, shown only this once: {code}")
    click.echo("Save it in your own list now. It cannot be shown again.")


@click.command("create-demo")
@click.argument("email")
@with_appcontext
def create_demo_command(email):
    """Create the Demo Student and print its password once."""
    email = _valid_email_or_refuse(email)
    with _database_errors():
        # D51: there is one Demo Student, so reset-demo can never
        # touch more than one account.
        if users.demo_student_exists():
            raise _refusal("A Demo Student already exists.")
        _refuse_if_email_taken(email)

        password = secrets.token_urlsafe(PASSWORD_BYTES)
        # R1b: the Demo Student never signs up, so the creator consents
        # on its behalf and consented_at is its creation time.
        users.create_user(
            email, password, role=users.STUDENT, is_demo=True, consented=True
        )
    _print_password("Demo Student", email, password)


def _valid_email_or_refuse(raw_email):
    email = users.normalize_email(raw_email)
    if email is None:
        raise _refusal(
            "That is not a valid email. Use one @ with a dot after it, "
            "for example test01@example.com."
        )
    return email


def _refuse_if_email_taken(email):
    if users.email_is_taken(email):
        raise _refusal(f"{email} already has an account.")


def _refusal(reason):
    return click.ClickException(f"{reason} Nothing was changed.")


@contextmanager
def _database_errors():
    """Turn database errors into a short message instead of a stack
    trace (rules.md section 8). The messages never hold a password or a
    code, because nothing secret is passed to the database in plain text.
    """
    try:
        yield
    except sqlite3.IntegrityError:
        # Only reached if two runs race past the checks above.
        raise _refusal("The database refused the change: that email "
                       "may already have an account.")
    except sqlite3.OperationalError as error:
        raise click.ClickException(
            f"Could not use the database at {_database_path()} ({error}). "
            "If it has no tables yet, run flask init-db first. "
            "Nothing was changed."
        )


def _print_password(account, email, password):
    # The database path is printed so it is always clear whether this
    # ran against dev or production (architecture.md: run deliberately).
    click.echo(f"{account} created for {email} in {_database_path()}.")
    click.echo(f"Password, shown only this once: {password}")
    click.echo("Save it in your own list now. It cannot be shown again.")


def _database_path():
    return current_app.config["DATABASE_PATH"]
