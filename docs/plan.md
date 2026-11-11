# Career Roadmap: plan

A web app for 10–15 invited IT students in Jordan. A student pastes a real job posting, the AI turns it into a 10-day plan of 30-minute tasks, and each day unlocks only when the student submits a link to the work they did. The hard parts: the AI plan must be checked before anyone sees it, a student must never edit past work or see another student's, and it all has to run at zero cost on a free host, live on Demo Night.

## Read in this order

| | File | What it answers |
|---|---|---|
| **Start here** | [`brief.md`](brief.md) | The problem, who has it, and what success means |
| Then | [`scope.md`](scope.md) | The limits, and what we are not building |
| | [`requirements.md`](requirements.md) | What it must do and never do, each with a test |
| | [`screens.md`](screens.md) | The six screens |
| | [`data-model.md`](data-model.md) | What we store |
| | [`architecture.md`](architecture.md) | The pieces and who talks to who |
| | [`stack.md`](stack.md) | What we build with, and what we rejected |
| | [`rules.md`](rules.md) | How code is written |
| **Background** | [`research.md`](research.md) | The alternatives and the gap |
| **Living** | [`progress.md`](progress.md) | Where things stand. Paste this first in a new chat |
| | [`decisions.md`](decisions.md) | Every choice and every rejected idea |
| | [`workflow.md`](workflow.md) | Branches, commits, pull requests, environments |
| | [`prompt-log.md`](prompt-log.md) | The prompts that shaped the project |

## Schedule

Weeks 1–4 decide. Weeks 5–7 build: three build weeks. A student has up to **14 days** to finish 10 daily tasks (D64), and success is measured just before Demo Night in week 8. **So testers must start on day 1 of week 7**, and the student loop must be live by the end of week 6.

The riskiest piece is a real AI call from the free host (A5), so it is proven first, before any screen is built around it.

| Week | Goal |
|---|---|
| 4 | Design every screen and its four states (`design.md`). Cut the work into tickets (`tickets/`). |
| 5 | Tickets 01–05: skeleton, **AI spike and first deploy** (D55), creator scripts, sign-up, log in. |
| 6 | Tickets 06–12: templates, Roadmap, submitting evidence, Completion, AI plan with fallback, states, privacy tests. Deploy. Invite testers at the end of the week. |
| 7 | **Test starts on day 1 of week 7:** all invite codes sent that day (D63, D64). Ticket 13–14: progress view and the remaining scripts. Bug fixes only, on `fix/*` branches. No nudging testers (D62). |
| 8 | Measure against `brief.md` section 4 on the last day before Demo Night (date: to be confirmed). Rehearse the demo on production (reset Demo Student between runs) and on dev. **Demo Night.** |

## If behind schedule, cut in this order

1. The job posting popup on the Roadmap screen
2. Choosing again before day 1
3. The creator progress view: read progress with SQL queries instead
4. The second template

**Never cut:** sign-up and login, the AI plan with its fallback (unless the spike fails on every provider, D55), submitting evidence, the privacy rules, the first deploy.
