"""Reading and writing the invite_codes table (data-model.md)."""

import hashlib
import secrets
from contextlib import closing

from .db import get_connection, utc_now

# Students type the code by hand, so letters and digits that look alike
# (0/O, 1/I/L) are left out.
CODE_ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"
CODE_LENGTH = 12
GROUP_SIZE = 4


def generate_invite_code():
    """A new random code, printed as ABCD-EFGH-JKMN."""
    characters = "".join(
        secrets.choice(CODE_ALPHABET) for _ in range(CODE_LENGTH)
    )
    groups = [
        characters[start:start + GROUP_SIZE]
        for start in range(0, CODE_LENGTH, GROUP_SIZE)
    ]
    return "-".join(groups)


def hash_invite_code(code):
    """Normalise a code and return its SHA-256 hash.

    Sign-up (ticket 04) uses this same function, so "abcd efgh-jkmn"
    and "ABCD-EFGH-JKMN" match. SHA-256 without a salt, unlike the
    password hash, so sign-up can find a code with WHERE code_hash = ?.
    That is safe because every code is random, not chosen by a person.
    """
    normalized = "".join(code.split()).replace("-", "").upper()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def save_invite_code(code):
    """Store only the hash of a new, unused code and return its id.

    R1: the real code is never stored.
    """
    with closing(get_connection()) as connection:
        with connection:
            cursor = connection.execute(
                "INSERT INTO invite_codes (code_hash, created_at)"
                " VALUES (?, ?)",
                (hash_invite_code(code), utc_now()),
            )
    return cursor.lastrowid
