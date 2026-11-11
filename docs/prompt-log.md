# Prompt Log

Every prompt used to think this project through, in order: what I asked, and what I decided because of it.

---

## Task 01 — Find the project

### 1. Interrogation prompt
**Asked:** "I am choosing a project to build over the next 8 weeks. Do not propose anything yet. Ask me one question at a time until you understand: the problem, who has it, what they do today instead, and what would count as solved. Stop and wait for my answer after each question. When you have enough, summarise it back to me in my own words and tell me what you still do not know."
**Decided:** Problem 1 is IT students who can't move from studying to working. The model asked why ChatGPT's plans fail and whether the bottleneck is knowing or doing.

### 2. Answering the open questions
**Asked:** Answered the model's unknowns and suggested a mentor network.
**Decided:** The real issue is execution and accountability, not planning. Focus on Jordan. Success at week 8 = 5–10 students finish a 14-day roadmap and one project. Mentor network postponed: it is a second project in itself.

### 3. Market-data constraint
**Asked:** I can't collect market data in 8 weeks, so the student should paste a job posting instead.
**Decided:** A real job posting is the input. The plan is split into 30-minute daily tasks. Help gives hints only, never full solutions.

### 4. Problem 2: pharmacy expiry dates
**Asked:** Same interrogation for expiry dates in a small community pharmacy.
**Decided:** The real problem is entering dates quickly at receiving, not alerts. Must be a standalone tool.

### 5. Problem 3: group-project fairness
**Asked:** Same interrogation for one student doing all the work in group projects.
**Decided:** Tracking must be passive and visible to the whole team. I dropped my idea of tracking people without them knowing.

### 6. Comparing the three
**Asked:** Compare the three problems side by side.
**Decided:** Chose Problem 1, because I know this pain from the inside and can reach the users.

> The Task 01 scope-block prompt isn't recorded here. If I find it, I'll add it as 6b.

---

## Task 02 — The brief, and a home for it

### 7. Sceptical manager review
**Asked:** "Here is my BRD. Do not rewrite it. Read it as the manager who has to approve it and who is sceptical. List: what is unclear, what is assumed without evidence, and what would make you refuse to fund it. Then ask me the three questions you most need answered."
**Decided:** The BRD was weak. Success was described as features, there was no evidence beyond my own experience, it had 5 components, and only one risk. It had also lost things I decided in Task 01.

### 8. Answering the three questions → brief.md
**Asked:** Answered the three questions and asked for a six-section brief.md.
**Decided:** Success = 5–10 students complete the 14 days plus a reviewed project. Failure = zero completions, or everyone quits within 4 days. Scope cut to 2 components: plan from a job posting, and daily 30-minute tasks that count only with an upload. IT students only.

### 9. research.md and workflow.md
**Asked:** Research ChatGPT, roadmap.sh and Coursera/YouTube, and write workflow rules.
**Decided:** The difference: they give a plan; mine requires daily proof of work. Don't rebuild what exists (use an LLM, link to roadmap.sh).

### 10. Checking against Task 02
**Asked:** Do the files meet the Task 02 requirements?
**Decided:** Content is covered. Still missing: pushing the repo, trying the competitors myself, and the workflow holes prompt.

### 11. Reworking for a solo developer
**Asked:** I work alone, adjust everything for that.
**Decided:** GitHub Issues as tickets. Model review plus a self-check after a break instead of a teammate. Manual deploy until hosting is chosen. Added solo-developer risk to the brief.

---
## Task 03 — The folder, finished

### 12. Drafting the six files
**Asked:** Wrote scope, requirements, screens, data model, architecture, stack, rules, decisions, progress and plan with the model, starting from brief.md.
**Decided:** First version: access-code login, templates, and custom plans prepared by me by hand.

### 13. Reading the folder back
**Asked:** I did not understand my own files, so I asked the model to explain each one simply, then check it against Task 03.
**Decided:** requirements.md had no "Done when" lines; plan.md was a schedule, not an index; progress.md was not four lines; scope.md forbade things I now wanted.

### 14. Changing the product
**Asked:** I wanted a real website with sign-up, and plans per country.
**Decided:** AI generates the plan inside the app from the posting (Gemini free tier). Sign-up with email, password and an invite code. 10–15 students, success = 3 completions. Country plans dropped: they need market data, and a local posting is already local.

### 15. Rewriting the files
**Asked:** Rewrite each file for the new decisions, and check the free host can reach the AI first.
**Decided:** PythonAnywhere's free allowlist includes Gemini. A plan is fixed after day 1, because a reset would delete submissions (N3). Old decisions kept, and replaced by D33–D43.

### 16. Updating the Task 02 files
**Asked:** Update brief, research, workflow and README so they don't contradict the new docs.
**Decided:** Evidence is a link, not an upload. Interviews removed; the week-8 trial tests the assumption instead.

### 17. Fresh-chat test
**Asked:** The Task 03 test prompt, in a new incognito chat, with the whole /docs folder.
**Decided:** First run: half the files still described the old product, so I replaced them. Second run: it understood the product, and found real gaps (Demo Student rehearsals, consent record, creator account, AI timeouts and limits). Answered in D46–D54.

### 18. Third fresh-chat test
**Asked:** The same test, after replacing the old files.
**Decided:** The model said the folder is coherent. Its sharper questions became D55–D63: AI spike first with backups, `unlock` as the only allowed change, outages don't burn attempts, non-IT postings refused, no nudging testers.

## Still to run
- [ ] Fresh-chat test on the whole /docs folder (Task 03)
- [ ] Workflow holes prompt on workflow.md (Task 02)
- [ ] Try each competitor for 10 minutes, then update research.md (Task 02)

## Task 04 — Design and backlog

### 19. Designing the Roadmap screen first
**Asked:** Mock up the main screen from brief, screens, requirements and data-model, then list what was decided for me and any field not in the data model.
**Decided:** The screen had no picture of where the 10 days lead, so I added `project_goal` (D65). Plans cut from 14 to 10 days to fit three build weeks (D64).

### 20. Choosing a look
**Asked:** Show several styles side by side.
**Decided:** Tried seven; chose "Sky & lilac" (D67). Rejected Butter & rose because it read as aimed at girls, and the testers are mixed.

### 21. The other five screens and their four states
**Asked:** Design each screen with Empty, Loading, Error and Full.
**Decided:** Wrote all of them in design.md. Where a state does not apply (no Loading on Completion), I wrote why instead of inventing one.

### 22. Cutting tickets
**Asked:** Cut the design into tickets with Why, Done when and Touches.
**Decided:** 14 tickets. The student loop works without AI after ticket 08; the AI spike comes second to answer the biggest risk early.