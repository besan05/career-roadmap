# Decisions

Every decision that shapes the project, with the reason and what was rejected. Newest at the bottom. A decision is changed only by adding a new one that replaces it.

## Problem and scope

| # | Date | Decision | Why | Rejected |
|---|---|---|---|---|
| D1 | 2026-10-16 | Build the career roadmap for IT students | A problem I and my peers live with; testers are easy to reach | Pharmacy expiry capture (strongest data, but not my own problem); group-project fairness (hardest to measure in 8 weeks) |
| D2 | 2026-10-16 | A real job posting is the input; no market data collection | One person cannot curate market data in 8 weeks; a real posting ties the plan to real demand | Building a market data pipeline |
| D3 | 2026-10-16 | Mentor network deferred until after the 8 weeks | A two-sided marketplace is a second project | Building it in the MVP |
| D4 | 2026-10-22 | MVP has two components: plan from a job description, and daily tasks with evidence | A sceptical review found five components too many | Skills assessment, mock interviews, advanced analysis |
| D5 | 2026-10-22 | IT students only | Engineering students need different roadmaps | IT and Engineering |

## Product

| # | Date | Decision | Why | Rejected |
|---|---|---|---|---|
| D6 | 2026-10-29 | No AI generation inside the app. Pre-written templates load instantly; custom plans are prepared by hand with my AI subscription and loaded as JSON | A paid API breaks the "no other paid services" limit | Paid API; free-tier API (open option for later, not a requirement) |
| D7 | 2026-10-29 | Days unlock by completion, not by calendar | The goal is finishing 14 steps, not matching dates | Calendar-based days |
| D8 | 2026-10-29 | No notifications, reminders or "welcome back" banners | Needs a sending service; keeps the app calm | Email reminders; return banner |
| D9 | 2026-10-29 | Evidence is links only | No file storage, no storage cost | Image uploads |
| D10 | 2026-10-29 | Login by access code, stored hashed | Password reset needs email; hashing protects the creator view if the database leaks | Email and password; plain-text codes |
| D11 | 2026-10-29 | Invite-only | A test with 5–10 known students | Public sign-up |
| D12 | 2026-10-29 | Desktop browser first, English only | Students code on laptops; tools are in English | Mobile layout; Arabic |
| D13 | 2026-10-29 | No skill-level rating | The template defines the path for the role | Self-rating; levelled templates |
| D14 | 2026-10-29 | A submission locks immediately; a confirmation step comes first; only the creator can unlock | Keeps the record honest (N3a) | Editable submissions |
| D15 | 2026-10-29 | Any valid link unlocks the next day; the creator reviews the work at the end | Automatic checking is out of scope; I am the reviewer | AI grading; manual approval each day |
| D16 | 2026-10-29 | A completion counts only within 21 days of starting, and after my review | Sequence-based days need a cut-off for the week-8 measurement | No cut-off; 14 days |
| D17 | 2026-10-29 | A student cannot change target in the app | Keeps the data simple | A "change target" button |
| D18 | 2026-10-29 | Custom plans take up to 24 hours; the screen says so | I prepare them by hand | No promised time |
| D19 | 2026-10-29 | Students stored by label only (e.g. "Student 01") | Smaller privacy risk (N1) | Real names |

## Data

| # | Date | Decision | Why | Rejected |
|---|---|---|---|---|
| D20 | 2026-10-30 | Picking a template copies its 14 days into the student's roadmap | A student's record of what they were asked must not change | Pointing to the template |
| D21 | 2026-10-30 | Unlocked submissions are kept and marked replaced, never overwritten | Keeps first-submission times honest (N3b) | Overwriting |
| D22 | 2026-10-30 | `reviewed_at` is a timestamp, not yes/no | Records when the review happened, at no extra cost | A boolean |
| D23 | 2026-10-30 | A custom plan's `started_at` is when I load it | My 24-hour preparation should not count against the student's 21 days | Start at request time |
| D24 | 2026-10-30 | Resetting a target deletes the roadmap, allowed **only before any submission exists** | No evidence exists yet, so the "never delete submissions" rule still holds | Inactive old roadmaps |

## Architecture and stack

| # | Date | Decision | Why | Rejected |
|---|---|---|---|---|
| D25 | 2026-10-30 | One app (pages, rules and data access in one program) | Fewest moving parts for one person to build and demo | Browser + hosted database service; separate frontend and backend |
| D26 | 2026-10-30 | Creator actions are command-line scripts that validate input | Prevents typos breaking a plan, without building an admin UI | Editing the database by hand; admin dashboard |
| D27 | 2026-10-30 | Sessions last 7 days, with Log out on every screen | Convenient on own laptops; limited risk on shared lab computers | Until logout; until browser closes |
| D28 | 2026-10-30 | Demo Night: student journey on production as "Demo Student"; creator view from dev with fake data | Evidence links can reveal real students' identities (N1) | Showing the real progress view |
| D29 | 2026-10-30 | Python, Flask, SQLite, hosted on PythonAnywhere free | Files persist on disk, so SQLite works; Python is my strongest language | Render (files lost on spin-down; free Postgres expires after 30 days); Vercel (no SQLite); Node.js/Express |
| D30 | 2026-10-30 | Plain `sqlite3`, Jinja templates, plain CSS, no frontend framework | Five tables and six screens don't need more | SQLAlchemy; React |

## Workflow

| # | Date | Decision | Why | Rejected |
|---|---|---|---|---|
| D31 | 2026-10-22 | Solo workflow: GitHub Issues as tickets; every pull request gets a model review, a self-check in a later session, and a local test run | No teammate to approve | Merging without review |
| D32 | 2026-10-30 | Manual deploy: pull `main` on PythonAnywhere, then reload | Free host; no automatic deploys needed for 5–10 users | Automatic deploys |

## Rework: real accounts and AI plans (2026-11-05)

Reading the folder back, the product felt too basic and the hand-made plans were hard to explain. These replace the decisions named in the "Replaces" column.

| # | Date | Decision | Why | Rejected | Replaces |
|---|---|---|---|---|---|
| D33 | 2026-11-05 | The AI generates the 14-day plan inside the app from the pasted posting, using the Gemini API free tier with no billing attached | The posting is what makes this different from roadmap.sh, so the plan must come from it automatically. Gemini is available in Jordan, and `.googleapis.com` is on PythonAnywhere's free allowlist (checked Nov 2026) | Plans prepared by hand; paid API; attaching billing | D6 |
| D34 | 2026-11-05 | Every AI plan is checked (role title, exactly 14 days, all fields) before saving; one retry; then the student is offered templates | The AI can return broken plans; a student must never see one | Showing raw AI output; unlimited retries | — |
| D35 | 2026-11-05 | Only the posting text and fixed instructions are sent to the AI; the key stays on the server | Free-tier inputs may be used by the provider; no personal data should leave the app | Sending the student's email or progress | — |
| D36 | 2026-11-05 | Accounts with email and password; passwords hashed. Email is the only personal data; no names | Access codes felt too basic for a real product | Access codes; storing names | D10, D19 |
| D37 | 2026-11-05 | Sign-up requires a single-use invite code; 10–15 invited students | Keeps the test limited and protects the AI free tier from strangers | Open sign-up; one shared code | D11 |
| D38 | 2026-11-05 | No password reset by email. A student who forgets asks me; `reset-password` sets a temporary one | Email needs a sending service | Email reset | — |
| D39 | 2026-11-05 | A student can discard their plan and choose again before day 1; after day 1 the plan is fixed | Before day 1 nothing is deleted but the plan; after it, a reset would delete submissions (N3) | No change at all; a creator reset after day 1 | D17, D24 |
| D40 | 2026-11-05 | A plan appears on the same visit; `started_at` is when it is created | There is no waiting time any more | — | D18, D23 |
| D41 | 2026-11-05 | Success at week 8 = at least 3 of the 10–15 invited students complete | Many testers drop out; this number is realistic and still proves something | 5–10 completions | — |
| D42 | 2026-11-05 | No plans tailored by country | Needs market data per country (ruled out in D2). A posting from the student's own country is already local | Country-based plans | — |
| D43 | 2026-11-05 | Call the AI with `requests`, not the official SDK | One HTTPS call; easier to read and to fake in tests | Gemini SDK | — |
| D44 | 2026-11-05 | Sign-up shows what data is stored and requires an "I agree" tick | Students must know what is kept before real sign-ups | Consent by message only | — |
| D45 | 2026-11-05 | "Reviewed" means the final link opens, matches the plan's project, and has a README | "The work exists" was too vague to measure | No written criteria | — |

## Answers to the fresh-chat test (2026-11-05)

A model that had never seen the project read the folder and asked these. These are my answers.

| # | Date | Decision | Why | Rejected | Replaces |
|---|---|---|---|---|---|
| D46 | 2026-11-05 | 30-second timeout per AI attempt, so about a minute at most with the retry. The single free worker blocking others meanwhile is accepted | 10–15 students each create a plan once or twice; collisions are rare | Background jobs; a paid worker | — |
| D47 | 2026-11-05 | At most 3 posting attempts per student before day 1; postings up to 6,000 characters; the prompt lives in `app/ai/prompt.txt`; the exact Gemini model is chosen in the week-3 spike | Protects the free tier, and keeps one place to change the prompt | Unlimited attempts; no length limit | — |
| D48 | 2026-11-05 | AI plans return `role_title` and `days` only. A template's `description` is read from its file for the template list and not stored | The database only keeps what a screen uses | A `description` column | — |
| D49 | 2026-11-05 | The creator account is made with a `create-creator` script | Same pattern as the other creator actions (D26) | Seeding it by hand | — |
| D50 | 2026-11-05 | Consent is stored as `users.consented_at` | A record of when each student agreed | Not storing it | — |
| D51 | 2026-11-05 | The Demo Student is marked with `is_demo`, created by `create-demo`, excluded from measurement, and reset between rehearsals by `reset-demo`, which refuses any other user. This is the only exception to N3 | The demo journey must be repeatable; the Demo Student is not a real student's work | A new Demo Student per rehearsal; no rehearsal on production | D28 (extends) |
| D52 | 2026-11-05 | Passwords at least 8 characters; emails stored and compared in lowercase; invite codes do not expire; no limit on failed logins | 10–15 known students over a few weeks; a lockout adds work and support. Known risk, accepted for the test | Login lockout; expiring codes | — |
| D53 | 2026-11-05 | The "View job posting" popup is in, and first on the cut list | Useful but not core | Removing it | — |
| D54 | 2026-11-05 | A live Gemini call from PythonAnywhere is proven in a week-3 spike, before any screen is built around it | It is the biggest unknown (A5) | Finding out at the first deploy in week 4 | — |

## Answers to the third fresh-chat test (2026-11-05)

| # | Date | Decision | Why | Rejected | Replaces |
|---|---|---|---|---|---|
| D55 | 2026-11-05 | The AI spike comes first in week 3, before the skeleton. If Gemini fails from PythonAnywhere, try Groq, then OpenRouter. If all fail, launch with templates only and record A5 as failed | Find out the biggest risk before building around it | Building screens first | — |
| D56 | 2026-11-05 | The only change ever made to a saved submission is `unlock` setting `replaced_at`, once | "Never update a submission" was not exactly true; the exception must be written down | Overwriting; deleting and re-adding | — |
| D57 | 2026-11-05 | A posting attempt counts only when the AI answers. The retry, timeouts, outages and rate limits do not count | A student should not lose attempts because the free tier was busy | Counting before the call | — |
| D58 | 2026-11-05 | The AI may refuse text that is not an IT job posting; the student sees a message and no plan is saved; a refusal counts as an attempt | Otherwise "hello" or a nursing posting gets a valid-looking IT plan | Accepting any text | — |
| D59 | 2026-11-05 | The prompt asks for: one project sized for 14 × 30 minutes, day 1 sets up a public repo, tasks point to existing free lessons, every day's evidence is linkable (R6b) | These decide plan quality; the code can only check structure | Leaving the prompt open | — |
| D60 | 2026-11-05 | The demo starts at log in as the Demo Student; no live sign-up | A live sign-up uses a real invite code and creates an account not marked `is_demo` | Signing up live | — |
| D61 | 2026-11-05 | Creator scripts are Flask CLI commands in `app/cli.py`; no `scripts/` folder | One place, shares the app's database code (matches stack.md) | A separate scripts folder | — |
| D62 | 2026-11-05 | No nudging testers during the test. I answer only when they contact me (e.g. a forgotten password) | A1 tests whether the evidence gate alone keeps students going; nudges would spoil it | Weekly check-ins | — |
| D63 | 2026-11-05 | All invite codes are sent on day 1 of week 6. Student data is deleted when the test ends, with no "keep it" option | Gives every tester the full 21 days before measuring; one clear consent text | Staggered invites; optional keeping | — |

## Task 04: fitting the schedule (2026-11-10)

| # | Date | Decision | Why | Rejected | Replaces |
|---|---|---|---|---|---|
| D64 | 2026-11-10 | Plans have **10 days**, not 14. A completion counts within **14 days** of starting, not 21. Testers start on day 1 of week 7 | There are only three build weeks (5–7). A 14-day plan with a 21-day window starting in week 6 left one build week and ran past Demo Night | Keeping 14 days and measuring only partial progress; starting the test before the app is finished | D16, the 14-day plan in D4 and D33 |
| D65 | 2026-11-11 | New field `roadmaps.project_goal`: one sentence on what the student will have built by day 10, shown on the Roadmap screen. Templates carry it; the AI must return it; a plan without it fails the check | Designing the Roadmap screen showed it lacked a destination: a list of tasks with no picture of the finished project. The data did not exist, so it was added on purpose | Leaving the screen without a goal; deriving the goal from the last day's title | — |
| D66 | 2026-11-11 | Pastel look: soft backgrounds (lavender, mint, peach, sky) with dark text and a deep lavender for buttons | Calm and encouraging for a learning tool; dark text keeps it readable | The first blue-and-grey design, which felt too plain | — |
| D67 | 2026-11-11 | Final look "Sky & lilac": sky-blue band at the top, lilac for the goal and the Today label, blue buttons, dark text. New layout: a top band with the role, the project goal, a progress ring and a 10-step journey line; today's task large on the left; a compact list of the 10 days on the right | Chosen from seven styles on the design canvas. The most neutral pastel for a mixed group of IT students; the first layout felt like a plain list | Midnight (dark), Sunrise (teal and coral), Peach & mint, Butter & rose (read as aimed at girls), Butter & teal | D66 |
| D68 | 2026-11-25 | Invite **5** students instead of 10–15. Success stays at least 3 completions | Less to manage alongside coursework, and the AI free tiers stay far below their limits. Fewer than 5 would mean almost everyone must finish | 3 students (all would have to finish); 10–15 | D37, D41 (numbers only) |
| D69 | 2026-11-25 | Backup AI: if Gemini fails twice, the app tries once with **Llama through Groq** (free tier, no billing), with the same plan check. Only if both fail does the student see the error and the templates | Fixed templates cannot cover every IT role (a QA student would get Frontend or Data Analyst). A second model makes "no plan" rare | Templates as the only fallback; a third provider | Extends D34, D55 |

## Arguments with the model

- **Country-based plans.** I wanted plans per country. The model pointed out this needs the market data I already ruled out in Task 01, and that a local posting already gives a local plan. I agreed (D42).
- **Manual plans.** The first draft had me preparing custom plans by hand. Reading it back, I could not explain the idea. I chose AI inside the app (D33), and the model checked the free host could reach the AI before I committed.
- **Reset after day 1.** The new requirements let the creator reset a plan after day 1. The model found this contradicted N3 (never delete submissions). I chose to fix the plan after day 1 instead (D39).
- **Limited sign-up.** I asked whether limiting the number adds much work. It is one field and one table, and it protects the AI free tier (D37).
- **Fresh-chat test.** The first test found half the files still described the old product. The second found real gaps: the Demo Student could not rehearse twice, consent was not stored, and nothing created the creator account (D46–D54). The third test found the folder coherent, and raised sharper questions: whether `unlock` breaks the "never change a submission" rule, whether outages burn attempts, and what happens with a non-IT posting (D55–D63).

## Assumptions to test

Written down so the test can prove them wrong:

- **A1 (from D8):** the evidence gate alone keeps students going, without reminders. The brief says students quit when "nobody asks where are you." If testers stall, revisit D8 first.
- **A2:** students will accept a template when the AI fails.
- **A3:** 14 tasks of about 30 minutes produce a project worth reviewing.
- **A4 (from D33):** AI plans from real local postings are good enough without my review.
- **A5 (from D33):** the Gemini free tier stays available, and reachable from PythonAnywhere, until Demo Night.

## Follow-ups from these decisions

- [x] ~~README and `brief.md`: custom plans within 24 hours (D6)~~ Replaced by D33.
- [x] `brief.md`: sections 2, 4 and 5 updated for D33, D37 and D41.
- [x] README: one-liner and status updated.
- [ ] Week-3 spike: one real AI call from PythonAnywhere (D54, D55, A5).
- [x] Plans shortened to 10 days (D64): all docs, README, brief and workflow updated.
- [ ] Add `GROQ_API_KEY=replace-me` to `.env.example` in workflow.md (D69).
- [ ] Confirm the Demo Night date and write it in `plan.md`.
