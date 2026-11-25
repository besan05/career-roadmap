"""TEMPORARY: the ticket 02 AI spike page.

Sends one fixed question to Gemini and once to Llama through Groq, and
shows both answers, to prove the free host can reach the AI (A5, D55).

Never merged into main: it is run from the feature branch on
PythonAnywhere, then deleted before the pull request is opened (ticket 02,
option A). It is registered only when APP_ENV=production and
SPIKE_PAGE=on (see create_app), so it never runs on a laptop.

Accepted exception to rules.md section 3, for this page only: the route
calls app/ai directly, with no Rules layer in between.
"""

import os
import time

from flask import Blueprint, current_app, render_template

from ..ai import client

bp = Blueprint("spike", __name__)

# N7: fixed, with nothing personal in it.
SPIKE_QUESTION = "Reply with exactly one word: ready"


@bp.get("/spike")
def spike_page():
    return render_template("spike.html", question=SPIKE_QUESTION, results=None)


@bp.post("/spike")
def run_spike():
    results = [
        _try_provider("Gemini", "GEMINI_MODEL", client.ask_gemini),
        _try_provider("Groq (Llama)", "GROQ_MODEL", client.ask_groq),
    ]
    return render_template(
        "spike.html", question=SPIKE_QUESTION, results=results
    )


def _try_provider(provider, model_setting, ask):
    started = time.monotonic()
    result = {
        "provider": provider,
        # The model name is not a secret, so it is safe to show.
        "model": os.environ.get(model_setting, "(not set)"),
        "ok": False,
        "answer": None,
        "kind": None,
        "status_code": None,
    }
    try:
        result["answer"] = ask(SPIKE_QUESTION)
        result["ok"] = True
    except client.AIError as error:
        result["kind"] = error.kind
        result["status_code"] = error.status_code
        # rules.md section 8: what went wrong and where, never a key.
        current_app.logger.warning("AI spike failed: %s", error)
    result["seconds"] = round(time.monotonic() - started, 1)
    return result
