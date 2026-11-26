# How I Work

Rules for the 8-week MVP. One developer (me), with the AI model as a working partner. Two environments: `dev` (local) and `production` (deployed).

## 0. Tickets

- Every piece of work is a **GitHub Issue** in this repo, before any code is written.
- An issue has a number, a one-line title, and a short "done when" checklist.
- No issue, no branch.

## 1. Branches

| Branch | Purpose | Rules |
|---|---|---|
| `main` | Always working. Production is deployed from it. | Never commit to it directly. Changes arrive only through a pull request. |
| `feature/<issue>-<short-name>` | New functionality. Example: `feature/12-daily-task-upload` | Branch from `main`. One issue per branch. Delete after merge. |
| `fix/<issue>-<short-name>` | Bug fixes. Example: `fix/18-plan-date-offset` | Branch from `main`. Change only what the bug needs. Delete after merge. |

- Lowercase, hyphen-separated names only.
- Only one open branch at a time. Finish or close it before starting another.
- A branch open longer than 5 days is either merged, split into smaller issues, or closed.

## 2. Commits

Format:

```
<type>: <what changed, in plain words, max 72 chars>

<optional body: why the change was needed>
```

| Type | Use for |
|---|---|
| `feat` | New user-facing behaviour |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code change with no behaviour change |
| `test` | Adding or fixing tests |

Good:

```
feat: generate 14-day plan from pasted job description
fix: reject task completion without a valid link
```

Never: `wip`, `update`, `changes`, `fix stuff`, `misc`, `final`, `asdf`, `.`

- One logical change per commit.
- Never commit secrets, `.env` files, or real student data.

## 3. Pull Requests

One issue, one branch, one pull request. I open a pull request even though I work alone, so every change to `main` has a record of what changed and why.

**Opening**

- Title uses the commit format: `feat: daily task submission`.
- First line links the issue: `Closes #12`.
- Description answers:
  1. **What** changed.
  2. **Why** (the issue or brief section).
  3. **What to check**: steps to test it locally.
- Add a screenshot for any UI change.
- Keep it small: aim for under 400 changed lines.

**Review (solo)**

Nothing merges straight after writing it. Before merging:

1. **Model review.** Paste the diff to the model with: *"Review this pull request against workflow.md, rules.md and requirements.md. List bugs, rule breaks, and anything out of scope. Do not rewrite it."* Fix or reply to every point.
2. **Self-check after a break.** Re-read the diff in a later session, not the one I wrote it in.
3. **Run it locally.** Follow the "What to check" steps myself.

**Merging**

- Merge only when all three review steps are done.
- Squash and merge, keeping the title as the commit message. Delete the branch.
- Check production after deploying. If it breaks, revert first, then fix in a new `fix/*` branch.

## 4. Environments

| | `dev` | `production` |
|---|---|---|
| **Where** | My laptop | PythonAnywhere, free account ([`stack.md`](stack.md)) |
| **Data** | Fake seed data only (fake students, sample job postings) | Real test students |
| **AI calls** | Saved fake answers by default; a separate dev key for occasional real calls | Gemini free tier, production key |
| **How it gets there** | Running locally | Manual: pull `main` in the PythonAnywhere console, then reload the web app |
| **Secrets** | Local `.env` | `.env` created in the PythonAnywhere console, never committed |

No staging environment for the MVP. To make up for it, every change is tested locally with fake data before it reaches `main`.

### Secret management

- `.env` is listed in `.gitignore` from the first commit and never committed.
- `.env.example` is committed with every variable name and placeholder values, for example:

```
  SECRET_KEY=replace-me
  DATABASE_PATH=instance/dev.db
  GEMINI_API_KEY=replace-me
  AI_MODE=fake
  APP_ENV=dev
  GROQ_API_KEY=replace-me
  GEMINI_MODEL=replace-me
  GROQ_MODEL=replace-me
```

- Every new variable goes into `.env.example` in the same pull request that introduces it.
- Dev and production use **separate** keys and databases. Local work never points at production data.
- Secrets are never pasted into the model, chat, commits, screenshots or issues.
- If a secret is committed by mistake: rotate it immediately, then remove it from the history.

### Data rules

- Real student data exists only in production.
- Never copy production data into dev.
- Submitted links and progress are deleted on request, and when the test period ends unless the student agrees otherwise.

## 5. Decided since this file was first written

- **Hosting:** PythonAnywhere, free account (D29).
- **Who reviews student projects:** me, at the end of each student's 14 days (D15).

## 6. Not decided yet

- **Automated checks (lint, tests on every push):** add once there is code to check. Until then, "run it locally" is the check.