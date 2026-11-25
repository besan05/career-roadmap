"""Smoke tests: the app starts, and flask init-db creates every table."""

import sqlite3
from contextlib import closing

import pytest

from app import create_app

# Every table and field in docs/data-model.md.
EXPECTED_COLUMNS = {
    "users": {
        "id", "email", "password_hash", "role", "is_demo",
        "consented_at", "posting_attempts", "created_at",
    },
    "invite_codes": {"id", "code_hash", "created_at", "used_by", "used_at"},
    "roadmaps": {
        "id", "user_id", "source", "template_id", "role_title",
        "project_goal", "job_posting", "started_at", "reviewed_at",
    },
    "roadmap_days": {
        "id", "roadmap_id", "day_number", "title", "instructions",
        "expected_evidence",
    },
    "submissions": {
        "id", "roadmap_day_id", "url", "submitted_at", "replaced_at",
    },
}


@pytest.fixture
def app(tmp_path):
    # A throwaway database per test, never dev.db or prod.db (rules.md 9).
    return create_app({
        "TESTING": True,
        "SECRET_KEY": "test-only-not-a-secret",
        "DATABASE_PATH": str(tmp_path / "test.db"),
    })


def read_columns(database_path, table):
    with closing(sqlite3.connect(database_path)) as connection:
        rows = connection.execute(
            "SELECT name FROM pragma_table_info(?)", (table,)
        ).fetchall()
    return {row[0] for row in rows}


def test_placeholder_page_loads(app):
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert b"Career Roadmap" in response.data


def test_init_db_creates_every_table_and_field(app):
    result = app.test_cli_runner().invoke(args=["init-db"])

    assert result.exit_code == 0, result.output
    for table, expected in EXPECTED_COLUMNS.items():
        assert read_columns(app.config["DATABASE_PATH"], table) == expected


def test_init_db_twice_changes_nothing(app):
    runner = app.test_cli_runner()
    runner.invoke(args=["init-db"])

    second = runner.invoke(args=["init-db"])

    assert second.exit_code != 0
    assert "nothing was changed" in second.output
