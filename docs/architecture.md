# Architecture

The shape of the system: what parts exist and what each is responsible for. Specific tools and languages are in [`stack.md`](stack.md).

## At a glance

```
┌──────────────┐        ┌───────────────────────────────────────────┐
│   Browser    │ HTTPS  │                 One app                   │
│ (student or  │◀──────▶│                                           │
│   creator)   │        │  Pages ─▶ Accounts & session ─▶ Rules     │
└──────────────┘        │                                  │    │   │
                        │                        Data access  AI client
                        └──────────────────────────────┼─────────┼──┘
                                                       │         │
┌──────────────┐                               ┌───────▼──────┐  │  ┌─────────────┐
│ Creator      │──── validate, then write ────▶│   Database   │  └─▶│  AI model   │
│ scripts      │                               └──────────────┘     │ (free tier) │
└──────────────┘                                                    └─────────────┘
       plans/  (template JSON files in the repo)
```

## Parts

| Part | Responsible for | Never does |
|---|---|---|
| **Browser** | Shows pages, sends forms. Light checks for quick feedback (e.g. "is this a URL?"). | Decides anything. Every check is repeated on the server. Never sees the AI key. |
| **Pages** | The 6 screens in [`screens.md`](screens.md). Sends each user to the right screen after login. | Reads the database or calls the AI directly. |
| **Accounts & session** | Sign-up with an invite code and consent, login with email and password, logout. Keeps the user logged in for **7 days** or until **Log out**. Knows if the user is a student or the creator. | Stores passwords or invite codes in plain text. |
| **Rules** | Everything in [`requirements.md`](requirements.md) that must be enforced: plan checks, attempt limits, current day only, server timestamps, no edits, own data only, creator-only view. | Trusts anything the browser sends about time, user or day. |
| **AI client** | Sends a pasted posting with the instructions in `app/ai/prompt.txt` to the AI model and returns its answer. 30-second timeout per attempt. | Sends anything personal (N7). Saves anything. Decides whether a plan is valid: that is Rules' job. |
| **Data access** | All reads and writes to the database, following [`data-model.md`](data-model.md). | Changes a submission, except `unlock` setting `replaced_at` once. Deletes one, except through `reset-demo`. |
| **Database** | Stores users, invite codes, roadmaps, days and submissions. | Holds files or names. |
| **AI model** | Gemini first; Llama through Groq as the backup (D69). Turns a posting into a role title and a 10-day plan in the agreed JSON shape. | Is trusted: its answer is always checked before saving. |
| **plans/** | Pre-written 10-day templates as JSON files in the repo. | Changes a student's plan after it has been copied. |
| **Creator scripts** | The creator's actions, run from the command line. Each validates its input before writing. | Runs inside the web app or has a screen. |

## Creator scripts

All scripts are Flask CLI commands registered in the app (`flask create-invite`), in `app/cli.py`. There is no separate scripts folder.

| Script | Does | Checks before writing |
|---|---|---|
| `create-creator <email>` | Creates the creator account and prints a password once | No creator exists yet |
| `create-invite` | Creates an invite code and prints it once | — |
| `create-demo <email>` | Creates the Demo Student and prints a password once | No Demo Student exists yet |
| `check-template <file.json>` | Validates a template without writing anything | Role title; project goal; exactly 10 days, numbered 1–10, all fields present |
| `reset-password <email>` | Sets a temporary password and prints it once | User exists |
| `unlock <email> <day>` | Marks the active submission replaced | Day has an active submission |
| `mark-reviewed <email>` | Sets `reviewed_at` | All 10 days completed |
| `reset-demo` | Deletes the Demo Student's plan and submissions, resets attempts | Only touches the user with `is_demo = yes` (D51) |

Codes and passwords are printed once and never stored in plain text. I keep my own list outside the app.

## Main flows

### Signing up

1. Student enters email, password and invite code, and ticks "I agree".
2. Accounts checks: the code exists and is unused, the email (in lowercase) has no account, the password has at least 8 characters, the box is ticked.
3. In one step: the account is created with the consent time, the password is hashed, the code is marked used.
4. A session starts; Pages opens **Choose your target**.

Any failed check → no account is created, and the student sees why.

### Logging in

1. Student enters email and password.
2. Accounts checks the password against the stored hash.
3. On match: a session starts (7 days); Pages sends the user to their landing screen.
4. On no match: error message, no session.

### Getting a plan from a posting

1. Student pastes a posting and presses **Create my plan**.
2. Rules check: logged in, no roadmap yet, posting not empty and at most 6,000 characters, fewer than 3 counted posting attempts so far.
3. AI client sends the posting and the instructions in `app/ai/prompt.txt` to the AI model (30-second timeout).
4. If the AI answers, the attempt is counted once (the retry below never counts again). Timeouts, outages and rate limits are not counted.
5. If the AI refused (not an IT job posting) → nothing is saved; the student sees the R5b message.
6. Rules check the answer: a role title, a project goal, exactly 10 days, numbered 1–10, all fields filled.
7. If the check fails or the call times out, steps 3 and 6 run once more with Gemini. If that fails too, they run once with the backup model (Llama through Groq) (D69).
8. Valid → a roadmap and its 10 days are saved with `started_at` from the server; **Roadmap** opens on day 1.
9. Second failure or AI error → nothing is saved; the student sees a short message and the templates.

While steps 4–7 run, the browser shows a loading message and the button is disabled. The single free worker is busy for up to about a minute (D46).

### Picking a template

1. Student picks a role.
2. Rules check they have no roadmap.
3. The template's 10 days are **copied** into a new roadmap, with `started_at` set by the server.
4. Roadmap screen opens on day 1.

### Choosing again (before day 1 only)

1. Student presses **Choose a different plan**.
2. Rules check that no submission exists for this roadmap.
3. The roadmap and its days are deleted; **Choose your target** opens. The attempt count stays.

### Submitting evidence

1. Student enters a link and confirms.
2. Rules check: logged in, the day belongs to this student, it is their **current** day, the link is a valid URL.
3. Data access saves the submission with the **server's** time.
4. The next day unlocks; after day 10, the Completion screen opens.

Any failed check → nothing is saved, and the student sees an error.

## Where rules are enforced

All of these run on the server, inside **Rules**, on every request:

| Rule | Requirement |
|---|---|
| Sign-up needs an unused invite code, a valid password and consent | R1, R1b |
| Only logged-in users see anything beyond Sign up and Log in | R2, N5 |
| At most 3 posting attempts; postings up to 6,000 characters | R5 |
| An AI plan is saved only if it passes the check | R6 |
| A student reads only their own data | N1 |
| Only the creator opens the progress view | N5 |
| Evidence is accepted only for the current day | N3 |
| Submission time comes from the server | N4 |
| No path changes a submission except `unlock` (sets `replaced_at` once), and none deletes one except `reset-demo` | N3 |
| The AI key and personal data never leave the server | N6, N7 |

## Environments

| | `dev` | `production` |
|---|---|---|
| Runs on | My laptop | PythonAnywhere, free account (see `stack.md`) |
| Database | Local, fake data only | Hosted, real test students |
| AI | Saved fake answers by default; a separate dev key for occasional real tests | Production key, free tier |
| Users | Fake students + me | Invited students + me + **Demo Student** |
| Scripts point at | Local database | Production database, run deliberately |

Never point local work at production data. Secrets live in `.env`, different per environment (see [`workflow.md`](workflow.md)).

## Demo Night

| Part of the demo | Where | Why |
|---|---|---|
| Student journey (log in, paste a posting, get a plan, submit day 1). No live sign-up: it would use a real invite code and create an account not marked `is_demo` | **Production**, as **Demo Student** | Proves the deployed app and the AI step work live |
| Before each rehearsal and before the demo | Run `reset-demo` | Day 1 fixes the plan, so the journey can only be shown again after a reset |
| If the AI fails live | The template fallback appears | Shows R7 working; the demo continues with a template |
| Creator progress view | **Dev**, with fake data | Real evidence links can reveal students' identities (N1) |
| Backup if the internet fails | **Dev** for everything, with saved AI answers | The demo still happens |

The **Demo Student** is excluded from all test measurements (`is_demo`).
