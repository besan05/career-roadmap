"""Reading and writing the users table (data-model.md)."""

from contextlib import closing

from werkzeug.security import generate_password_hash

from .db import get_connection, utc_now

STUDENT = "student"
CREATOR = "creator"


def normalize_email(raw_email):
    """Return the email trimmed and in lowercase, or None if it is not
    valid.

    Valid means one @ with a dot after it (D52). Sign-up and login
    (ticket 04) use this same function, so an email is always stored
    and compared the same way (R1).
    """
    email = raw_email.strip().lower()
    if any(character.isspace() for character in email):
        return None

    local_part, at_sign, domain = email.partition("@")
    if not at_sign or not local_part or "@" in domain:
        return None

    name, dot, ending = domain.rpartition(".")
    if not dot or not name or not ending:
        return None
    return email


def email_is_taken(email):
    # R1: emails are stored in lowercase, so a plain comparison is
    # already case-insensitive as long as callers use normalize_email.
    with closing(get_connection()) as connection:
        row = connection.execute(
            "SELECT 1 FROM users WHERE email = ?", (email,)
        ).fetchone()
    return row is not None


def creator_exists():
    with closing(get_connection()) as connection:
        row = connection.execute(
            "SELECT 1 FROM users WHERE role = ? LIMIT 1", (CREATOR,)
        ).fetchone()
    return row is not None


def demo_student_exists():
    with closing(get_connection()) as connection:
        row = connection.execute(
            "SELECT 1 FROM users WHERE is_demo = 1 LIMIT 1"
        ).fetchone()
    return row is not None


def create_user(email, password, role, is_demo=False, consented=False):
    """Insert a user and return its id.

    The password is hashed here, so no caller can store it in plain
    text (R1). With consented=True, consented_at is the creation time
    (R1b). Raises sqlite3.IntegrityError if the email is already used.
    """
    created_at = utc_now()
    consented_at = created_at if consented else None
    with closing(get_connection()) as connection:
        # The connection as a context manager commits on success and
        # rolls back on any error, so nothing is half-saved (rules.md 8).
        with connection:
            cursor = connection.execute(
                "INSERT INTO users"
                " (email, password_hash, role, is_demo, consented_at,"
                "  created_at)"
                " VALUES (?, ?, ?, ?, ?, ?)",
                (
                    email,
                    generate_password_hash(password),
                    role,
                    1 if is_demo else 0,
                    consented_at,
                    created_at,
                ),
            )
    return cursor.lastrowid
