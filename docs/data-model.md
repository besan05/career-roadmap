# Data Model

What the app stores and how the pieces relate. Supports [`requirements.md`](requirements.md) and [`screens.md`](screens.md).

## Principles

- **Store only what a requirement needs.** A student's email is the only personal data stored. No names or phone numbers.
- **Nothing a student submits is ever deleted or edited.** Corrections are added beside the original (N3, N4). The only exception is the Demo Student (D51).
- **A student's plan is a copy.** Templates and AI plans are copied into the student's roadmap; later changes to a template never change it.
- **Text only.** Evidence is a link. No files are stored.

## Overview

```
invite_codes ──0..1:1── users ──1:0..1── roadmaps ──1:14── roadmap_days ──1:many── submissions

plans/*.json  (template files in the repo, copied into roadmap_days)
```

## Tables

### `users`

Students, the Demo Student and the creator.

| Field | Type | Notes |
|---|---|---|
| `id` | id | Primary key |
| `email` | text, unique | Stored in lowercase. Used to log in |
| `password_hash` | text | Hashed. The real password is never stored |
| `role` | `student` \| `creator` | Only `creator` can open the progress view (N5) |
| `is_demo` | yes/no | Yes only for the Demo Student. Excluded from measurement |
| `consented_at` | timestamp, nullable | When the student ticked "I agree" (R1b). Empty only for the creator |
| `posting_attempts` | integer | Counted attempts from a posting before day 1: only when the AI answered. At most 3 (R5) |
| `created_at` | timestamp | Set by the server |

### `invite_codes`

Single-use codes that allow a student to sign up (R1). Codes do not expire.

| Field | Type | Notes |
|---|---|---|
| `id` | id | Primary key |
| `code_hash` | text, unique | Hashed. The real code is printed once and never stored |
| `created_at` | timestamp | Set by the server |
| `used_by` | → `users.id`, nullable | Empty = unused |
| `used_at` | timestamp, nullable | Set when a student signs up with it |

### `roadmaps`

One student's plan. A student has at most one.

| Field | Type | Notes |
|---|---|---|
| `id` | id | Primary key |
| `user_id` | → `users.id`, unique | One roadmap per student |
| `source` | `template` \| `posting` | |
| `template_id` | text, nullable | e.g. `junior-frontend`. Empty for posting-based plans |
| `role_title` | text | From the template, or from the AI. Shown at the top of the Roadmap screen |
| `job_posting` | text, nullable | Posting-based plans only. As pasted, up to 6,000 characters |
| `started_at` | timestamp | When the plan was created |
| `reviewed_at` | timestamp, nullable | Empty = not reviewed. Set by the creator (R18) |

### `roadmap_days`

The 14 steps of one roadmap.

| Field | Type | Notes |
|---|---|---|
| `id` | id | Primary key |
| `roadmap_id` | → `roadmaps.id` | |
| `day_number` | integer, 1–14 | Unique per roadmap |
| `title` | text | |
| `instructions` | text | About 30 minutes of work |
| `expected_evidence` | text | What link to submit, e.g. "GitHub commit adding the navbar" |

### `submissions`

Evidence links. Never deleted or edited.

| Field | Type | Notes |
|---|---|---|
| `id` | id | Primary key |
| `roadmap_day_id` | → `roadmap_days.id` | |
| `url` | text | Must start with `http://` or `https://` |
| `submitted_at` | timestamp | Set by the server, never by the student (N4) |
| `replaced_at` | timestamp, nullable | Empty = active. Set once by `unlock` (R17). The only field of a submission that ever changes |

**Rule:** each day has at most one active submission (`replaced_at` empty).

## Plan format

### Templates

Stored in the repo as `plans/<template_id>.json`, at least `junior-frontend` and `junior-data-analyst`. The `description` is read from the file for the template list on Choose your target; it is not stored in the database.

```json
{
  "template_id": "junior-frontend",
  "role_title": "Junior Frontend Developer",
  "description": "HTML, CSS, JavaScript and one deployed project.",
  "days": [
    {
      "day_number": 1,
      "title": "Set up your project repo",
      "instructions": "Create a public GitHub repo ...",
      "expected_evidence": "Link to the repo with a README"
    }
  ]
}
```

### AI plans

The AI is asked to return only `role_title` and `days`, in the same shape. No `template_id` or `description`.

A plan is valid only if it has a role title and exactly 14 days, numbered 1–14, each with all three fields filled (R6). An invalid plan is never saved.

## Derived values (calculated, not stored)

| Value | How |
|---|---|
| Completed day | Has an active submission |
| Current day | Lowest `day_number` without an active submission |
| Locked day | Any day after the current day |
| Days completed | Count of days with an active submission |
| Finished | All 14 days completed |
| First submission time of a day | Earliest `submitted_at` for that day, including replaced ones |

## Landing state after login

| Condition | Screen |
|---|---|
| `role = creator` | Progress view |
| No roadmap | Choose your target |
| Roadmap, not finished | Roadmap |
| Roadmap, finished | Completion |

## Choosing again (R9)

Before day 1 is submitted, a student can discard their plan: the roadmap and its days are deleted. This is safe because no submissions exist yet. After day 1, the plan is fixed. Discarding does not reset `posting_attempts`.

## Measurement (brief, section 4)

Users with `is_demo = yes` are excluded from every number.

- **Completed:** first submission time of day 14 is within **21 days** of `started_at`, and `reviewed_at` is set.
- **Success:** at least 3 students completed.
- **Days taken per step:** difference between first submission times of consecutive days.
- **Dropout day:** current day of a student who has not finished after 21 days.

## Creator actions in the database

All done with the scripts in [`architecture.md`](architecture.md).

| Action | Change |
|---|---|
| Create the creator account | Insert a `users` row with `role = creator` |
| Create an invite code | Insert an `invite_codes` row |
| Create the Demo Student | Insert a `users` row with `is_demo = yes` |
| Reset a password | Replace `users.password_hash` |
| Unlock a mistake | Set `replaced_at` on the active submission |
| Mark reviewed | Set `roadmaps.reviewed_at` |
| Reset the Demo Student | Delete the Demo Student's roadmap, days and submissions, and set `posting_attempts` to 0. Refused for any other user (D51) |

## After the test

Student data is deleted on request, and when the test ends (R1b).
