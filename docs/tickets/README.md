# Tickets

Every piece of work for the build weeks, cut from [`../design.md`](../design.md). Each ticket becomes one GitHub Issue, one branch and one pull request ([`../workflow.md`](../workflow.md)).

## Order

| # | Ticket | Week |
|---|---|---|
| 01 | [Project skeleton](01-project-skeleton.md) | 5 |
| 02 | [AI spike and first deploy](02-ai-spike-and-first-deploy.md) | 5 |
| 03 | [Creator, invite and demo scripts](03-creator-account-scripts.md) | 5 |
| 04 | [Sign up with invite code and consent](04-sign-up.md) | 5 |
| 05 | [Log in, log out and landing](05-log-in-and-out.md) | 5 |
| 06 | [Role templates and picking one](06-templates-and-choose-a-role.md) | 6 |
| 07 | [Roadmap screen](07-roadmap-screen.md) | 6 |
| 08 | [Submit a link and unlock the next day](08-submit-evidence.md) | 6 |
| 09 | [Completion screen](09-completion-screen.md) | 6 |
| 10 | [AI plan from a pasted posting](10-ai-plan-from-posting.md) | 6 |
| 11 | [Choose a different plan before day 1](11-choose-a-different-plan.md) | 6 |
| 12 | [Privacy and rule tests](12-privacy-and-rule-tests.md) | 6 |
| 13 | [Creator progress view](13-progress-view.md) | 7 |
| 14 | [Unlock, review, password and demo scripts](14-remaining-creator-scripts.md) | 7 |

**Why this order.** The student loop (sign up, pick a template, see the roadmap, submit a link, watch the next day unlock) works end to end after ticket 08, with no AI at all. That loop is what the test measures, so it comes first. The AI plan (10) comes after it, but the risky part, reaching the AI from the free host, is proven at the very start in ticket 02. The creator view and the last scripts (13, 14) are needed only once the test is running, in week 7.

**Gate:** tickets 01–12 are done and deployed by the end of week 6. Invites go out on day 1 of week 7 (D63, D64).

## First three

1. **01 · Project skeleton.** Boring on purpose: nothing works without it, and it is the smallest possible first pull request.
2. **02 · AI spike and first deploy.** The biggest unknown, answered before anything depends on it. If it fails, I switch provider or go templates-only in week 5, not in week 7.
3. **03 · Creator, invite and demo scripts.** Without an account and an invite code, no one can sign up, so 04 and 05 cannot be tested.

## If behind schedule, cut in this order

1. The job posting popup (part of 07)
2. 11 · Choose a different plan
3. 13 · Progress view (read progress with SQL instead)
4. The second template (part of 06)

**Never cut:** 01–05, 08, 10 with its fallback, 12.
