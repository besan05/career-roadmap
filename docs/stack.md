# Stack

The tools that build [`architecture.md`](architecture.md). Every choice costs **$0** ([`scope.md`](scope.md)).

## Summary

| Layer | Choice | Why |
|---|---|---|
| Language | **Python 3.11+** | The language I know best. Required by the host. |
| Web framework | **Flask** | Small, one app, no build step. Fits the single-app architecture. |
| Pages | **Jinja2 templates** (comes with Flask), server-rendered HTML | No frontend framework to learn or deploy. |
| Styling | **Plain CSS**, one file | 6 screens don't need a framework. |
| Browser scripting | **A few lines of plain JavaScript** | Only for the submit confirmation, the job posting popup (`<dialog>`) and disabling the button while the AI works. |
| Database | **SQLite**, via Python's built-in `sqlite3` | One file, no server, no cost. Enough for 10–15 students. |
| Schema | `schema.sql` in the repo | Tables from [`data-model.md`](data-model.md), created by one command. |
| Sessions | Flask's signed cookie session, 7-day lifetime | Built in. No extra service. |
| Password hashing | `werkzeug.security` (comes with Flask) | Built in, salted hashes. |
| Invite code hashing | `hashlib` SHA-256 (standard library) | Codes are random, so a plain hash is safe and can be looked up directly. |
| AI model | **Google Gemini API, free tier**, a Flash-class model, no billing attached | Free, available in Jordan, and reachable from the free host. The exact model is chosen in the week-3 spike, from what the free tier offers then, and recorded in `decisions.md`. |
| AI prompt | `app/ai/prompt.txt` in the repo | One place to read and change the instructions sent to the AI. |
| Calling the AI | **requests** | One plain HTTPS call with a JSON body. Simpler to read and to fake in tests than a full SDK. |
| Form protection | **Flask-WTF** (`CSRFProtect`) | Stops other sites submitting forms as a logged-in student. |
| Config and secrets | **python-dotenv** + `.env` | Matches [`workflow.md`](workflow.md). |
| Creator scripts | **Flask CLI commands** (`flask create-invite`) | Built into Flask; shares the app's database code. |
| Tests | **pytest** | Standard for Python. |
| Hosting | **PythonAnywhere**, free account | Keeps files on disk, so SQLite data persists. Python-native. |
| Source control | GitHub (`besan05`) | Already set up. |

## Dependencies

Everything else is in Python's standard library or comes with Flask.

```
flask
flask-wtf
python-dotenv
requests
pytest        # dev only
```

## Environments

| | `dev` | `production` |
|---|---|---|
| Runs | `flask run` on my laptop | PythonAnywhere web app |
| Database file | `instance/dev.db` (fake data) | `instance/prod.db` on PythonAnywhere |
| AI | Saved fake answers by default (`AI_MODE=fake`); dev key for occasional real calls | Production key |
| `.env` | Local file | Created in the PythonAnywhere console, never committed |
| Deploy | — | Manual: pull `main` in the PythonAnywhere console, then reload the web app |

`instance/` and `.env` are in `.gitignore`. No database file is ever committed.

## Implementation notes

- **Timestamps** are stored in UTC and shown in Jordan time (UTC+3).
- **Emails** are stored in lowercase.
- **Invite codes** are generated with Python's `secrets` module and printed once.
- **URL check:** `urllib.parse` confirms the scheme is `http` or `https` and there is a domain. The same check runs in the browser and on the server.
- **AI call:** a timeout of **30 seconds per attempt**, so at most about a minute with the one retry. The prompt asks for JSON only, in the shape in `data-model.md`. The answer is parsed and checked by Rules before anything is saved.

## Limits of the free services, and what I do about them

| Limit | What I do |
|---|---|
| **Free PythonAnywhere accounts can only reach sites on its allowlist** | `.googleapis.com` (Gemini) is on it, checked November 2026. Groq, OpenRouter and Mistral are on it too, as backups. Proven with one real call in the week-3 spike. |
| Gemini's free tier allows only a few requests per minute without billing | Enough for 10–15 students with at most 3 posting attempts each. If two students hit the limit together, the second sees the template fallback. Billing is never attached. |
| Free-tier AI terms may allow Google to use what is sent | Only the posting text is sent, never personal data (N7). |
| One web app, one worker | While one student waits for the AI (up to about a minute), others wait too. Accepted for 10–15 students (D46). |
| The web app expires after **one month** if not renewed | Renew from the PythonAnywhere dashboard. Calendar reminder every 3 weeks, and in the week before Demo Night. |
| 512 MiB disk | The database is text only; it stays far below this. |
| Limited daily CPU time | Waiting for the AI uses almost no CPU. Pages are simple. |
| No scheduled tasks for new free accounts | No automatic backups. I download `prod.db` manually once a week. |
| Support is community-only | Keep `dev` working as the Demo Night backup. |

## Ruled out

| Option | Why not |
|---|---|
| Render (free) | Files are lost on every spin-down, restart or redeploy, so SQLite data would disappear. Free Postgres expires after 30 days. |
| Vercel | Does not support SQLite. |
| Node.js / Express | Fine, but the chosen host runs Python, and Python is my strongest language. |
| An ORM (SQLAlchemy) | Five tables don't need it; plain SQL is easier to read and review. |
| React or another frontend framework | A second build step and more to learn, for 6 simple screens. |
| A paid AI API, or Gemini with billing attached | Breaks the zero-cost rule. |
| The official Gemini SDK | More dependencies than one HTTPS call needs. |
| Plans prepared by hand | Replaced by the AI step (D33). |
