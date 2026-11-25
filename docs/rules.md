# Rules

How code is written on this project. Written for the AI model and for me. Read this before every coding session.

## 1. Before writing anything

- Read, in this order: [`progress.md`](progress.md), [`brief.md`](brief.md), [`scope.md`](scope.md), [`requirements.md`](requirements.md), [`screens.md`](screens.md), [`data-model.md`](data-model.md), [`architecture.md`](architecture.md), [`stack.md`](stack.md), [`decisions.md`](decisions.md), and the GitHub Issue being worked on.
- Work on **one issue at a time**, on its own branch ([`workflow.md`](workflow.md)).
- **If something is unclear, ask me instead of deciding it yourself.** Every answer that settles a question goes into [`decisions.md`](decisions.md).

## 2. Scope

- Build only what [`requirements.md`](requirements.md) asks for. Anything in the "Out" list of [`scope.md`](scope.md) is never added, even partly or "for later."
- If a task seems to need something out of scope, stop and say so. Do not quietly shrink or extend the task.
- No new dependency without a line in `decisions.md` explaining why the standard library or Flask can't do it.

## 3. File structure

```
app/
  routes/      one file per screen group: auth, plan, roadmap, creator
  rules/       the logic: plan checks, day unlocking, link validation
  data/        all database access
  ai/          the only code that talks to the AI model, plus prompt.txt
  templates/   Jinja2 templates, one per screen
  static/      CSS and the little JavaScript we use
  cli.py       creator scripts as Flask CLI commands (see architecture.md)
plans/         role templates as JSON, one file per role
tests/
  fake_ai/     saved AI answers, good and broken, used by tests and dev
```

- Routes call rules; rules call data and ai. Nothing else talks to the database or the AI.
- Templates only display. No logic beyond loops and simple conditions.

## 4. Naming

- Python style: PEP 8. Short functions.
- English names that say what they hold: `current_day`, not `cd`; `submitted_at`, not `time`.
- Files and folders: lowercase with underscores.

## 5. Comments

- Comments explain **why**, not what.
- Every rule from `requirements.md` that the code enforces names it in a comment, e.g. `# N3: a completed day can never be changed`.

## 6. Security

| Rule | Why |
|---|---|
| Every check happens on the server, even if the browser also checks | Browsers can be bypassed |
| Every query for student data filters by the logged-in user's id from the session, never by an id from the URL or form | N1, N5 |
| Every creator route checks `role = creator` first | N5 |
| Passwords are stored hashed with Werkzeug's password helpers (part of Flask), and have at least 8 characters | R1 |
| Emails are stored and compared in lowercase | R1 |
| An invite code is marked used in the same step that creates the account | R1 |
| SQL uses parameters (`?`), never string formatting or f-strings | Prevents SQL injection |
| `submitted_at` is set by the server. The only change to a submission is `unlock` setting `replaced_at` once; the only deletion is `reset-demo` | N3, N4 |
| Evidence is accepted only for the current day | N3 |
| Jinja autoescaping stays on; never mark user input `\|safe` | Prevents injected scripts |
| Every form has CSRF protection | Prevents forged submissions |
| Secrets come from environment variables only | [`workflow.md`](workflow.md) |

## 7. The AI

- Only code in `app/ai/` calls the AI model, and only from the server. The key never reaches the browser (N6).
- Only the pasted posting and the instructions in `app/ai/prompt.txt` are sent. Never an email, name or progress (N7).
- Every response is checked before saving: a role title, a project goal, exactly 10 days, in order, each with a title, instructions and expected evidence (R6).
- Each attempt times out after 30 seconds. A failed check or timeout is retried once with Gemini, then tried once with the backup model, Llama through Groq. If that fails too, the template fallback is shown (R7, D69). The student never sees raw AI output or an error page.
- A posting attempt is counted once, only when the AI answers. The retry, timeouts, outages and rate limits never count. After 3 counted attempts, only templates are offered (R5).
- If the AI refuses a text that is not an IT job posting, nothing is saved and the R5b message is shown.
- Tests never call the real AI. They use the saved answers in `tests/fake_ai/`, including broken ones.

## 8. Error handling

- Every error the student sees says what to do next, not only what went wrong.
- Students never see a stack trace, an SQL error or an AI error message. They see a short friendly message.
- Errors are logged on the server with what went wrong and where, but never with a password, a secret, an AI key or a pasted posting.
- Invalid input is rejected before anything is saved. Nothing is half-saved.

## 9. Data

- Code and tests use **fake data only**. Fake students use addresses like `test01@example.com`. No real names or emails, anywhere.
- Never connect local code or tests to the production database.
- Timestamps are stored in UTC and displayed in Jordan time.

## 10. Tests

A pull request is not ready unless tests cover what it changed. These must always have tests:

- Sign-up: valid invite code, wrong code, used code, email already registered (in another letter case), password under 8 characters, consent not ticked.
- Login: correct password, wrong password, logged out.
- AI plans: a valid response is saved; a response with 13 or 15 days, a missing field or no role title is rejected; two failures show the templates; a refusal saves nothing; a timeout does not count as an attempt; after 3 counted attempts only templates are shown.
- Submitting: valid link, invalid link, locked day, already completed day.
- Privacy: a student cannot read another student's roadmap or reach the creator view, even by typing the address.

## 11. When the model proposes code

- Say which files change and why, in one line each.
- Change only what the issue needs. Do not reformat or rewrite unrelated files.
- End with the steps to test it locally.
- If a rule here blocks the task, say which rule. Do not work around it.

## 12. Never

- Never decide something unclear on your own. Ask.
- Never add anything from the "Out" list of `scope.md`.
- Never put a secret or the AI key in code, logs, the browser or a commit.
- Never send personal data to the AI.
- Never show raw AI output to a student without the check in section 7.
- Never let a student change or delete a submission.
- Never use real student data outside production.
- Never promise or imply a job or an interview on any screen (N2).

## 13. Done means

- The issue's "done when" checklist is met.
- Tests pass locally.
- The pull request follows [`workflow.md`](workflow.md), including the model review and a self-check in a later session.
- [`progress.md`](progress.md) is updated.
