"""The only code that talks to the AI models (rules.md section 7).

First version, from ticket 02: one call to Gemini and one to the backup,
Llama through Groq (D69). Ticket 10 adds prompt.txt, the plan check, the
retry and the fallback on top of these two functions.

Keys and model names come from environment variables only, loaded from
.env by create_app (rules.md section 6). Model names are in .env so a
different model can be tried on the server without a commit.
"""

import os

import requests

# Each attempt times out after 30 seconds (rules.md section 7).
TIMEOUT_SECONDS = 30

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "{model}:generateContent"
)
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


class AIError(Exception):
    """Any failed AI call.

    kind is one of:
      not_configured  a key or model name is missing from .env
      proxy_blocked   PythonAnywhere's proxy refused the site (a host failure, A5)
      connection      the site could not be reached at all (a host failure, A5)
      timeout         no answer within 30 seconds
      http_error      the site answered with an error, e.g. 429 for a quota
      bad_response    the answer was not in the expected shape

    N6: the message holds only the provider, the kind and the HTTP status,
    never a key, a request URL or the response body, so it is safe to log.
    """

    def __init__(self, provider, kind, status_code=None):
        self.provider = provider
        self.kind = kind
        self.status_code = status_code
        status = f", HTTP {status_code}" if status_code is not None else ""
        super().__init__(f"{provider}: {kind}{status}")


def ask_gemini(text):
    """Send text to Gemini and return its answer as a string."""
    key = _setting("Gemini", "GEMINI_API_KEY")
    model = _setting("Gemini", "GEMINI_MODEL")
    data = _post(
        "Gemini",
        GEMINI_URL.format(model=model),
        # N6: the key goes in a header, not in the URL, because requests
        # puts the URL into its error messages and those can reach a log.
        headers={"x-goog-api-key": key},
        # N7: only the text we are given is sent, nothing about the user.
        body={"contents": [{"parts": [{"text": text}]}]},
    )
    return _read_answer(
        "Gemini", lambda: data["candidates"][0]["content"]["parts"][0]["text"]
    )


def ask_groq(text):
    """Send text to Llama through Groq and return its answer as a string."""
    key = _setting("Groq", "GROQ_API_KEY")
    model = _setting("Groq", "GROQ_MODEL")
    data = _post(
        "Groq",
        GROQ_URL,
        headers={"Authorization": f"Bearer {key}"},
        # N7: only the text we are given is sent, nothing about the user.
        body={"model": model, "messages": [{"role": "user", "content": text}]},
    )
    return _read_answer(
        "Groq", lambda: data["choices"][0]["message"]["content"]
    )


def _setting(provider, name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise AIError(provider, "not_configured")
    return value


def _post(provider, url, headers, body):
    """POST the JSON body and return the parsed JSON answer.

    Every requests error is turned into an AIError with `from None`, so
    the original exception, which can include the URL and headers, is
    never chained into a log (N6).
    """
    try:
        response = requests.post(
            url, headers=headers, json=body, timeout=TIMEOUT_SECONDS
        )
    except requests.exceptions.Timeout:
        raise AIError(provider, "timeout") from None
    # ProxyError is a kind of ConnectionError, so it is caught first:
    # it is how a free PythonAnywhere account sees a site not on its
    # allowlist, which is exactly what this ticket needs to tell apart.
    except requests.exceptions.ProxyError:
        raise AIError(provider, "proxy_blocked") from None
    except requests.exceptions.ConnectionError:
        raise AIError(provider, "connection") from None
    except requests.exceptions.RequestException:
        raise AIError(provider, "connection") from None

    if response.status_code != 200:
        raise AIError(provider, "http_error", response.status_code)
    try:
        return response.json()
    except ValueError:
        raise AIError(provider, "bad_response", response.status_code) from None


def _read_answer(provider, pick_text):
    try:
        text = pick_text()
    except (KeyError, IndexError, TypeError):
        raise AIError(provider, "bad_response", 200) from None
    if not isinstance(text, str) or not text.strip():
        raise AIError(provider, "bad_response", 200)
    return text
