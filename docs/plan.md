# Career Roadmap: plan

A web app for 10–15 invited IT students in Jordan. A student pastes a real job posting, the AI turns it into a 14-day plan of 30-minute tasks, and each day unlocks only when the student submits a link to the work they did. The hard parts: the AI plan must be checked before anyone sees it, a student must never edit past work or see another student's, and it all has to run at zero cost on a free host, live on Demo Night.

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

A student needs up to 21 days to finish (D16), and success is measured at week 8. **So testers must start at the beginning of week 6.** Weeks 3–5 build the student loop and put it live.

The riskiest piece is a real AI call from the free host (A5), so it is proven first, before any screen is built around it.

| Week | Goal |
|---|---|
| 3 | Finish the docs. **AI spike first:** a tiny app on PythonAnywhere makes one real Gemini call and prints the result. If Gemini fails from there, try Groq, then OpenRouter, the same week. If all fail, the app launches with templates only and A5 is recorded as failed (D55). Then the project skeleton: the app runs locally, the database is created, one test passes. |
| 4 | Sign-up with invite codes and consent, login, logout. `create-creator`, `create-invite`, `create-demo` scripts. Two templates. Choose your target (template path). **First deploy.** |
| 5 | AI plan from a posting, with the check, attempt limit and template fallback. Roadmap and submitting evidence. Completion screen. Privacy tests. Invite testers. |
| 6 | **Test starts on day 1 of week 6:** all invite codes sent that day (D63). Creator progress view; `unlock`, `mark-reviewed`, `reset-password`, `reset-demo` scripts. Bug fixes only, on `fix/*` branches. |
| 7 | Run the test: weekly backup, read the progress view, review finished work. No nudging testers; I only answer when they contact me (D62). Renew the web app. |
| 8 | Measure against `brief.md` section 4 on the last day before Demo Night (date: to be confirmed). Rehearse the demo on production (reset Demo Student between runs) and on dev. **Demo Night.** |

## If behind schedule, cut in this order

1. The job posting popup on the Roadmap screen
2. Choosing again before day 1
3. The creator progress view: read progress with SQL queries instead
4. The second template

**Never cut:** sign-up and login, the AI plan with its fallback (unless the spike fails on every provider, D55), submitting evidence, the privacy rules, the first deploy.
