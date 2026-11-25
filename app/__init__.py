"""Career Roadmap: the Flask app factory."""

import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask_wtf import CSRFProtect

from .cli import register_commands

PROJECT_ROOT = Path(__file__).resolve().parent.parent

csrf = CSRFProtect()


def create_app(test_config=None):
    """Build the app.

    Tests pass test_config with their own DATABASE_PATH, so they never
    touch dev.db or prod.db (rules.md section 9).
    """
    # Loaded explicitly because PythonAnywhere's web app does not go
    # through `flask run`, which would load .env on its own.
    load_dotenv(PROJECT_ROOT / ".env")

    app = Flask(__name__)
    # Secrets come from environment variables only (rules.md section 6).
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        DATABASE_PATH=os.environ.get("DATABASE_PATH"),
        APP_ENV=os.environ.get("APP_ENV", "dev"),
    )
    if test_config is not None:
        app.config.update(test_config)

    _check_required_config(app)
    app.config["DATABASE_PATH"] = _resolve_database_path(
        app.config["DATABASE_PATH"]
    )

    # Every form has CSRF protection (rules.md section 6).
    csrf.init_app(app)
    register_commands(app)

    # Temporary placeholder so `flask run` shows something.
    # Removed in ticket 06, when the real screens arrive.
    @app.route("/")
    def placeholder():
        return (
            "<!doctype html>"
            "<html lang='en'><head><meta charset='utf-8'>"
            "<title>Career Roadmap</title></head>"
            "<body><h1>Career Roadmap</h1>"
            "<p>The app is running. Screens arrive in later tickets.</p>"
            "</body></html>"
        )

    return app


def _check_required_config(app):
    for name in ("SECRET_KEY", "DATABASE_PATH"):
        if not app.config.get(name):
            raise RuntimeError(
                f"{name} is not set. Copy .env.example to .env "
                "and fill in the values."
            )


def _resolve_database_path(database_path):
    """Make a relative path relative to the project folder, not to
    wherever the app happens to be started from, and create its folder
    (instance/) if it is missing."""
    path = Path(database_path)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)
