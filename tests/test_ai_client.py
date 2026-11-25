"""The AI client: what it sends, and how it reports failures.

Tests never call the real AI (rules.md section 7): requests.post is
replaced in every test, and any call that slips through fails loudly.
"""

import pytest
import requests

from app.ai import client

GEMINI_KEY = "test-gemini-key-not-real"
GROQ_KEY = "test-groq-key-not-real"
QUESTION = "Reply with exactly one word: ready"


class FakeResponse:
    def __init__(self, status_code=200, data=None, bad_json=False):
        self.status_code = status_code
        self._data = data
        self._bad_json = bad_json

    def json(self):
        if self._bad_json:
            raise ValueError("not JSON")
        return self._data


class FakePost:
    """Stands in for requests.post and remembers how it was called."""

    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error
        self.calls = []

    def __call__(self, url, headers=None, json=None, timeout=None):
        self.calls.append(
            {"url": url, "headers": headers, "json": json, "timeout": timeout}
        )
        if self.error is not None:
            raise self.error
        return self.response


def gemini_answer(text):
    return {"candidates": [{"content": {"parts": [{"text": text}]}}]}


def groq_answer(text):
    return {"choices": [{"message": {"content": text}}]}


@pytest.fixture(autouse=True)
def settings(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", GEMINI_KEY)
    monkeypatch.setenv("GEMINI_MODEL", "test-gemini-model")
    monkeypatch.setenv("GROQ_API_KEY", GROQ_KEY)
    monkeypatch.setenv("GROQ_MODEL", "test-llama-model")


@pytest.fixture(autouse=True)
def no_real_calls(monkeypatch):
    def refuse(*args, **kwargs):
        raise AssertionError("A test tried to call the real AI")

    monkeypatch.setattr(client.requests, "post", refuse)


def use_fake(monkeypatch, fake):
    monkeypatch.setattr(client.requests, "post", fake)
    return fake


# --- Gemini -----------------------------------------------------------

def test_gemini_returns_the_answer(monkeypatch):
    fake = use_fake(monkeypatch, FakePost(FakeResponse(data=gemini_answer("ready"))))

    assert client.ask_gemini(QUESTION) == "ready"

    call = fake.calls[0]
    assert call["url"] == (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "test-gemini-model:generateContent"
    )
    assert call["headers"] == {"x-goog-api-key": GEMINI_KEY}
    assert call["timeout"] == 30


def test_gemini_key_is_never_in_the_url(monkeypatch):
    fake = use_fake(monkeypatch, FakePost(FakeResponse(data=gemini_answer("ready"))))

    client.ask_gemini(QUESTION)

    assert GEMINI_KEY not in fake.calls[0]["url"]
    assert "key=" not in fake.calls[0]["url"]


def test_gemini_sends_only_the_given_text(monkeypatch):
    # N7: nothing but the text goes to the AI.
    fake = use_fake(monkeypatch, FakePost(FakeResponse(data=gemini_answer("ready"))))

    client.ask_gemini(QUESTION)

    assert fake.calls[0]["json"] == {"contents": [{"parts": [{"text": QUESTION}]}]}


# --- Groq -------------------------------------------------------------

def test_groq_returns_the_answer(monkeypatch):
    fake = use_fake(monkeypatch, FakePost(FakeResponse(data=groq_answer("ready"))))

    assert client.ask_groq(QUESTION) == "ready"

    call = fake.calls[0]
    assert call["url"] == "https://api.groq.com/openai/v1/chat/completions"
    assert call["headers"] == {"Authorization": f"Bearer {GROQ_KEY}"}
    assert call["timeout"] == 30
    assert call["json"] == {
        "model": "test-llama-model",
        "messages": [{"role": "user", "content": QUESTION}],
    }


# --- Failures, for both providers ------------------------------------

PROVIDERS = [
    pytest.param(client.ask_gemini, gemini_answer, "GEMINI_API_KEY", "GEMINI_MODEL", id="gemini"),
    pytest.param(client.ask_groq, groq_answer, "GROQ_API_KEY", "GROQ_MODEL", id="groq"),
]


@pytest.mark.parametrize("ask, answer, key_name, model_name", PROVIDERS)
@pytest.mark.parametrize("missing", ["key", "model"])
def test_missing_setting_fails_without_calling(
    monkeypatch, ask, answer, key_name, model_name, missing
):
    monkeypatch.delenv(key_name if missing == "key" else model_name)
    # no_real_calls is still in place, so any call would fail the test.

    with pytest.raises(client.AIError) as caught:
        ask(QUESTION)

    assert caught.value.kind == "not_configured"


@pytest.mark.parametrize("ask, answer, key_name, model_name", PROVIDERS)
@pytest.mark.parametrize(
    "error, kind",
    [
        (requests.exceptions.Timeout(), "timeout"),
        (requests.exceptions.ProxyError(), "proxy_blocked"),
        (requests.exceptions.ConnectionError(), "connection"),
    ],
    ids=["timeout", "proxy", "connection"],
)
def test_network_failures_are_reported_by_kind(
    monkeypatch, ask, answer, key_name, model_name, error, kind
):
    use_fake(monkeypatch, FakePost(error=error))

    with pytest.raises(client.AIError) as caught:
        ask(QUESTION)

    assert caught.value.kind == kind
    assert caught.value.status_code is None


@pytest.mark.parametrize("ask, answer, key_name, model_name", PROVIDERS)
def test_rate_limit_is_an_http_error_with_its_status(
    monkeypatch, ask, answer, key_name, model_name
):
    use_fake(monkeypatch, FakePost(FakeResponse(status_code=429, data={})))

    with pytest.raises(client.AIError) as caught:
        ask(QUESTION)

    assert caught.value.kind == "http_error"
    assert caught.value.status_code == 429


@pytest.mark.parametrize("ask, answer, key_name, model_name", PROVIDERS)
@pytest.mark.parametrize(
    "response",
    [
        FakeResponse(bad_json=True),
        FakeResponse(data={}),
        FakeResponse(data={"candidates": [], "choices": []}),
    ],
    ids=["not-json", "empty", "no-answers"],
)
def test_unexpected_answer_shape_is_a_bad_response(
    monkeypatch, ask, answer, key_name, model_name, response
):
    use_fake(monkeypatch, FakePost(response))

    with pytest.raises(client.AIError) as caught:
        ask(QUESTION)

    assert caught.value.kind == "bad_response"


@pytest.mark.parametrize("ask, answer, key_name, model_name", PROVIDERS)
def test_empty_answer_is_a_bad_response(monkeypatch, ask, answer, key_name, model_name):
    use_fake(monkeypatch, FakePost(FakeResponse(data=answer("   "))))

    with pytest.raises(client.AIError) as caught:
        ask(QUESTION)

    assert caught.value.kind == "bad_response"


@pytest.mark.parametrize("ask, answer, key_name, model_name", PROVIDERS)
def test_error_message_never_holds_a_key(monkeypatch, ask, answer, key_name, model_name):
    # N6: the error is logged, so it must never carry a key.
    use_fake(monkeypatch, FakePost(FakeResponse(status_code=401, data={})))

    with pytest.raises(client.AIError) as caught:
        ask(QUESTION)

    message = str(caught.value)
    assert GEMINI_KEY not in message
    assert GROQ_KEY not in message
    assert caught.value.__cause__ is None
