# Team Workflow

Rules for the 8-week MVP. Two environments: `dev` (local) and `production` (deployed).

## 1. Branches

| Branch | Purpose | Rules |
|---|---|---|
| `main` | Always deployable. Every merge deploys to production. | Protected. No direct pushes. Changes arrive only through a reviewed pull request. |
| `feature/<ticket>-<short-name>` | New functionality. Example: `feature/12-daily-task-upload` | Branch from `main`. One ticket per branch. Delete after merge. |
| `fix/<ticket>-<short-name>` | Bug fixes. Example: `fix/18-plan-date-offset` | Branch from `main`. Keep the change limited to the bug. Delete after merge. |

- Lowercase, hyphen-separated names only.
- Rebase on `main` (or merge `main` in) before opening a pull request.
- A branch older than 5 days is either merged, split, or closed.

## 2. Commits

Format:

```
<type>: <what changed, imperative, max 72 chars>

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
fix: reject task completion without an upload
```

Forbidden as a whole message or as the only description: `wip`, `update`, `changes`, `fix stuff`, `misc`, `final`, `asdf`, `.`

- One logical change per commit.
- Never commit secrets, `.env` files, or real student data.

## 3. Pull Requests

**Opening**

- Title uses the commit format: `feat: daily task upload`.
- Link the ticket in the first line: `Closes #12`.
- Description answers three things:
  1. **What** changed.
  2. **Why** (link to the ticket or brief section).
  3. **How to test** it locally, step by step.
- Add a screenshot or short recording for any UI change.
- Keep it small: aim for under 400 changed lines.

**Merging**

- At least 1 approval from a teammate who did not write the code.
- All checks pass (build, lint, tests).
- No unresolved review comments.
- Squash and merge, keeping the title as the commit message.
- The author merges, then deletes the branch.
- Check production after merging. If it breaks, revert first and fix in a new `fix/*` branch.

## 4. Environments

| | `dev` | `production` |
|---|---|---|
| **Where** | Each developer's machine | Deployed hosting |
| **Data** | Fake seed data only (fake students, sample job postings) | Real test students |
| **AI calls** | Low-cost model or mocked responses | Production model |
| **Deployed by** | Running locally | Automatic on merge to `main` |
| **Secrets** | Local `.env` | Hosting provider's environment variable settings |

### Secret management

- `.env` is listed in `.gitignore` and never committed.
- `.env.example` is committed with every variable name and placeholder values, for example:

```
  DATABASE_URL=postgres://user:password@localhost:5432/roadmap_dev
  LLM_API_KEY=replace-me
  APP_ENV=dev
```

- Every new variable is added to `.env.example` in the same pull request that introduces it.
- Dev and production use **separate** keys and databases. Production keys never sit on a laptop.
- Secrets are shared privately through a password manager, never in chat, commits, screenshots or issues.
- If a secret is committed by mistake: rotate it immediately, then remove it from the history.

### Data rules

- Real student data exists only in production.
- Never copy production data into dev.
- Uploaded code and progress are deleted on request, and when the test period ends unless the student agrees otherwise.