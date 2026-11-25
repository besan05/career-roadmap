"""TEMPORARY (ticket 02): the AI spike page is off unless it is on purpose.

Deleted with app/routes/spike.py before ticket 02 closes.
"""

import pytest

from app import create_app
from app.ai import client


def make_app(tmp_path, app_env, spike_page):
    return create_app({
        "TESTING": True,
        "SECRET_KEY": "test-only-not-a-secret",
        "DATABASE_PATH": str(tmp_path / "test.db"),
        "APP_ENV": app_env,
        "SPIKE_PAGE": spike_page,
        # The real page has CSRF protection; turned off here only so the
        # test can post the form without a browser.
        "WTF_CSRF_ENABLED": False,
    })


@pytest.fixture(autouse=True)
def no_real_calls(monkeypatch):
    # rules.md section 7: tests never call the real AI.
    def refuse(*args, **kwargs):
        raise AssertionError("A test tried to call the real AI")

    monkeypatch.setattr(client.requests, "post", refuse)


@pytest.mark.parametrize(
    "app_env, spike_page",
    [("dev", "off"), ("dev", "on"), ("production", "off")],
)
def test_spike_page_is_not_there_unless_both_switches_are_on(
    tmp_path, app_env, spike_page
):
    test_client = make_app(tmp_path, app_env, spike_page).test_client()

    assert test_client.get("/spike").status_code == 404
    assert test_client.post("/spike").status_code == 404


def test_spike_page_opens_without_calling_the_ai(tmp_path):
    # no_real_calls would fail this test if opening the page called the AI.
    response = make_app(tmp_path, "production", "on").test_client().get("/spike")

    assert response.status_code == 200
    assert b"Ask Gemini and Groq once each" in response.data


def test_spike_page_shows_both_answers(tmp_path, monkeypatch):
    monkeypatch.setattr(client, "ask_gemini", lambda text: "ready from gemini")
    monkeypatch.setattr(client, "ask_groq", lambda text: "ready from groq")

    response = make_app(tmp_path, "production", "on").test_client().post("/spike")

    assert response.status_code == 200
    assert b"ready from gemini" in response.data
    assert b"ready from groq" in response.data


def test_spike_page_shows_a_failure_by_kind(tmp_path, monkeypatch):
    def blocked(text):
        raise client.AIError("Gemini", "proxy_blocked")

    monkeypatch.setattr(client, "ask_gemini", blocked)
    monkeypatch.setattr(client, "ask_groq", lambda text: "ready from groq")

    response = make_app(tmp_path, "production", "on").test_client().post("/spike")

    assert response.status_code == 200
    assert b"proxy_blocked" in response.data
    assert b"ready from groq" in response.data


def test_spike_page_escapes_the_answer(tmp_path, monkeypatch):
    # rules.md section 6: AI text is never trusted as HTML.
    monkeypatch.setattr(client, "ask_gemini", lambda text: "<script>x</script>")
    monkeypatch.setattr(client, "ask_groq", lambda text: "ready")

    response = make_app(tmp_path, "production", "on").test_client().post("/spike")

    assert b"<script>x</script>" not in response.data
    assert b"&lt;script&gt;" in response.data


def test_spike_form_is_rejected_without_a_csrf_token(tmp_path):
    # rules.md section 6: every form has CSRF protection.
    app = make_app(tmp_path, "production", "on")
    app.config["WTF_CSRF_ENABLED"] = True

    response = app.test_client().post("/spike")

    assert response.status_code == 400
