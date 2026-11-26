# Progress

**Last updated:** 2026-11-25 · **Week:** 5 of 8

- **Done:** Tasks 01–04. Task 05: tickets 01, 02 and 03 built, reviewed on GitHub and merged (PRs #1, #2, #3). The skeleton is live at https://besan05.pythonanywhere.com. The AI spike passed (A5): Gemini `gemini-3.5-flash-lite` and Groq `openai/gpt-oss-120b` both answer from PythonAnywhere (D70, D71). 52 tests pass. No new packages were approved; everything uses Flask, Werkzeug, `requests` and the standard library.
- **Doing:** creating the creator account and the 5 invite codes on production.
- **Next:** week 6, tickets 04–06: sign-up, log in and out, templates and choose a role.
- **Blocked:** nothing. Open: separate production AI keys, and the Demo Night date.

## Honest paragraph: what went wrong in Task 05

The coding model did good work, but not without supervision. In ticket 01 it planned to edit `docs/progress.md` and `docs/decisions.md` on its own, so I added "Do NOT edit anything in docs/" to every prompt after that. It added `app/data/db.py`, which was not in the plan; it told me, and I kept it. It never saw `requirements.md`, so the rule IDs in its schema comments were guessed and needed checking. My own mistakes were worse. I pasted a `SECRET_KEY` into a chat twice, and the first one also ended up in `.env.example` in PR #1 on a public repo. I only caught it when reviewing the pull request, sent it back, replaced it with `replace-me` and rotated the key (D79). The AI spike showed why a spike comes first. Groq no longer has a Llama chat model, so D69 was already out of date (D70). `gemini-3.5-flash` took 30 seconds for a one-word answer and then timed out, so the lite model replaced it (D71). In ticket 02 the model miscounted its tests in one table, and its docstrings still said "Llama" after the switch; I sent that back in PR #2. In ticket 03 it added `utc_now()` to `db.py` without planning it (disclosed, accepted). It also told me never to run the creator scripts against production, which is the opposite of architecture.md. I also used the same AI keys locally and on the server, which breaks my own workflow.md; that is now a follow-up.
