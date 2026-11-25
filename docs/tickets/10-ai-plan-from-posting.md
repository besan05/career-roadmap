# 10 · AI plan from a pasted posting

**Week:** 6

## Why

The posting is what makes this different from roadmap.sh (D33). Uses what ticket 02 proved (R5, R5b, R6, R6b, R7, N6, N7).

## Done when

- [ ] `app/ai/prompt.txt` asks for the four things in R6b and for JSON with `role_title`, `project_goal` and 10 days
- [ ] Only the posting text and the prompt are sent to the AI; never an email, name or progress (N7)
- [ ] A plan is saved only if it has a role title, a project goal and exactly 10 days with all fields (R6); otherwise Gemini is asked once more, then the backup model (Llama through Groq) once (D69)
- [ ] If all three tries fail, a timeout (30 seconds per try) or an outage shows the template fallback message; the student never sees raw AI output
- [ ] A refusal ("not an IT job posting") shows the R5b message and saves nothing
- [ ] Tries count only when the AI answers; after 3 counted tries only templates are offered (D57)
- [ ] Postings over 6,000 characters and empty postings are refused before any call
- [ ] The Loading and Error states of screen 3 match `design.md`
- [ ] Tests use the saved answers in `tests/fake_ai/` and never call the real AI

## Touches

`app/ai/client.py`, `app/ai/prompt.txt`, `app/rules/plans.py`, `app/routes/plan.py`, `app/templates/choose.html`, `tests/fake_ai/*.json`, `tests/test_ai_plans.py`. Data model: `roadmaps.job_posting`, `users.posting_attempts`.
