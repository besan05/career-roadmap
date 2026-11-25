"""Tests for the creator scripts: create-creator, create-invite and
create-demo (ticket 03)."""

import re
import sqlite3
from contextlib import closing
from pathlib import Path

import pytest
from werkzeug.security import check_password_hash

from app import create_app
from app.data.invites import CODE_ALPHABET, hash_invite_code
from app.data.users import normalize_email

PASSWORD_LINE = re.compile(r"^Password, shown only this once: (\S+)$", re.M)
CODE_LINE = re.compile(r"^Code, shown only this once: (\S+)$", re.M)


@pytest.fixture
def app(tmp_path):
    # A throwaway database per test, never dev.db or prod.db (rules.md 9).
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-only-not-a-secret",
        "DATABASE_PATH": str(tmp_path / "test.db"),
    })
    # Guard: stop at once if the test config ever stops winning over .env.
    assert Path(app.config["DATABASE_PATH"]).parent == tmp_path
    return app


@pytest.fixture
def runner(app):
    runner = app.test_cli_runner()
    result = runner.invoke(args=["init-db"])
    assert result.exit_code == 0, result.output
    return runner


def query(app, sql, parameters=()):
    with closing(sqlite3.connect(app.config["DATABASE_PATH"])) as connection:
        connection.row_factory = sqlite3.Row
        return connection.execute(sql, parameters).fetchall()


def every_stored_value(app):
    """Every value in every table, as text, to prove a secret is not in it."""
    table_rows = query(
        app, "SELECT name FROM sqlite_master WHERE type = 'table'"
    )
    tables = [row["name"] for row in table_rows]
    values = []
    for table in tables:
        for row in query(app, f"SELECT * FROM {table}"):
            values.extend(str(value) for value in row)
    return values


def printed_password(result):
    match = PASSWORD_LINE.search(result.output)
    assert match, result.output
    return match.group(1)


# normalize_email (reused by sign-up in ticket 04)

@pytest.mark.parametrize("raw, expected", [
    ("test01@example.com", "test01@example.com"),
    ("  Test01@Example.COM \n", "test01@example.com"),
    ("a@b.co", "a@b.co"),
])
def test_normalize_email_trims_and_lowercases(raw, expected):
    assert normalize_email(raw) == expected


@pytest.mark.parametrize("raw", [
    "", "test01", "test01@example", "@example.com", "test01@.com",
    "test01@example.", "a@b@example.com", "test 01@example.com",
])
def test_normalize_email_rejects_invalid(raw):
    assert normalize_email(raw) is None


# hash_invite_code (reused by sign-up in ticket 04)

def test_hash_invite_code_ignores_case_hyphens_and_spaces():
    expected = hash_invite_code("ABCD-EFGH-JKMN")

    assert hash_invite_code("abcd-efgh-jkmn") == expected
    assert hash_invite_code("ABCDEFGHJKMN") == expected
    assert hash_invite_code(" abcd efgh\tjkmn ") == expected
    assert hash_invite_code("ABCD-EFGH-JKMP") != expected


# create-creator

def test_create_creator_stores_only_a_hash(app, runner):
    result = runner.invoke(args=["create-creator", "  Creator@Example.com "])

    assert result.exit_code == 0, result.output
    password = printed_password(result)
    assert len(password) >= 8
    assert result.output.count(password) == 1

    [user] = query(app, "SELECT * FROM users")
    assert user["email"] == "creator@example.com"
    assert user["role"] == "creator"
    assert user["is_demo"] == 0
    assert user["consented_at"] is None
    assert user["created_at"]
    assert check_password_hash(user["password_hash"], password)
    assert password not in every_stored_value(app)


def test_second_creator_is_refused(app, runner):
    runner.invoke(args=["create-creator", "creator@example.com"])

    second = runner.invoke(args=["create-creator", "other@example.com"])

    assert second.exit_code != 0
    assert "already exists" in second.output
    assert "Nothing was changed" in second.output
    assert "Password" not in second.output
    assert len(query(app, "SELECT id FROM users")) == 1


def test_create_creator_refuses_an_email_in_use(app, runner):
    runner.invoke(args=["create-demo", "test01@example.com"])

    result = runner.invoke(args=["create-creator", "TEST01@example.com"])

    assert result.exit_code != 0
    assert "already has an account" in result.output
    assert "Password" not in result.output
    assert query(app, "SELECT id FROM users WHERE role = 'creator'") == []


def test_create_creator_refuses_an_invalid_email(app, runner):
    result = runner.invoke(args=["create-creator", "not-an-email"])

    assert result.exit_code != 0
    assert "not a valid email" in result.output
    assert "Password" not in result.output
    assert query(app, "SELECT id FROM users") == []


# create-invite

def test_create_invite_stores_only_a_hash(app, runner):
    result = runner.invoke(args=["create-invite"])

    assert result.exit_code == 0, result.output
    match = CODE_LINE.search(result.output)
    assert match, result.output
    code = match.group(1)
    assert re.fullmatch(r"[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}", code)
    assert set(code.replace("-", "")) <= set(CODE_ALPHABET)
    assert result.output.count(code) == 1

    [invite] = query(app, "SELECT * FROM invite_codes")
    assert invite["code_hash"] == hash_invite_code(code)
    assert invite["used_by"] is None
    assert invite["used_at"] is None
    assert invite["created_at"]
    stored = every_stored_value(app)
    assert code not in stored
    assert code.replace("-", "") not in stored


def test_each_invite_code_is_different(app, runner):
    first = CODE_LINE.search(runner.invoke(args=["create-invite"]).output)
    second = CODE_LINE.search(runner.invoke(args=["create-invite"]).output)

    assert first.group(1) != second.group(1)
    assert len(query(app, "SELECT id FROM invite_codes")) == 2


def test_create_invite_without_tables_is_refused(app):
    # No init-db, so the database file has no tables yet.
    result = app.test_cli_runner().invoke(args=["create-invite"])

    assert result.exit_code != 0
    assert "flask init-db" in result.output
    assert "Code, shown" not in result.output


# create-demo

def test_create_demo_marks_the_demo_student(app, runner):
    result = runner.invoke(args=["create-demo", "Demo@Example.com"])

    assert result.exit_code == 0, result.output
    password = printed_password(result)
    assert len(password) >= 8
    assert result.output.count(password) == 1

    [user] = query(app, "SELECT * FROM users")
    assert user["email"] == "demo@example.com"
    assert user["role"] == "student"
    assert user["is_demo"] == 1
    # The creator consents on the Demo Student's behalf (R1b).
    assert user["consented_at"] == user["created_at"]
    assert check_password_hash(user["password_hash"], password)
    assert password not in every_stored_value(app)


def test_second_demo_student_is_refused(app, runner):
    runner.invoke(args=["create-demo", "demo@example.com"])

    second = runner.invoke(args=["create-demo", "demo2@example.com"])

    assert second.exit_code != 0
    assert "already exists" in second.output
    assert "Password" not in second.output
    assert len(query(app, "SELECT id FROM users WHERE is_demo = 1")) == 1


def test_create_demo_refuses_an_email_in_use(app, runner):
    runner.invoke(args=["create-creator", "creator@example.com"])

    result = runner.invoke(args=["create-demo", "Creator@Example.com"])

    assert result.exit_code != 0
    assert "already has an account" in result.output
    assert "Password" not in result.output
    assert query(app, "SELECT id FROM users WHERE is_demo = 1") == []


# Nothing secret is logged

def test_passwords_and_codes_are_never_logged(runner, caplog):
    caplog.set_level("DEBUG")

    creator = runner.invoke(args=["create-creator", "creator@example.com"])
    demo = runner.invoke(args=["create-demo", "demo@example.com"])
    invite = runner.invoke(args=["create-invite"])

    secrets_printed = [
        printed_password(creator),
        printed_password(demo),
        CODE_LINE.search(invite.output).group(1),
    ]
    for secret in secrets_printed:
        assert secret not in caplog.text
