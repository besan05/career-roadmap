# 06 · Role templates and picking one

**Week:** 6

## Why

Templates are the fallback when the AI fails, and the fastest way for a student to start (R4, R8). With this ticket the student loop works end to end without any AI.

## Done when

- [ ] `plans/junior-frontend.json` and `plans/junior-data-analyst.json` exist, each with a role title, a project goal and exactly 10 days
- [ ] `flask check-template <file>` accepts both files and rejects a file with 9 days, a missing field or no project goal
- [ ] Choose your target (screen 3) shows both templates with their descriptions, in the Empty and Full states from `design.md`
- [ ] Picking a template copies its 10 days into a new roadmap with `started_at` from the server, then opens the Roadmap
- [ ] A student who already has a roadmap cannot create a second one

## Touches

`plans/*.json`, `app/cli.py`, `app/rules/plans.py`, `app/routes/plan.py`, `app/templates/choose.html`, `tests/test_templates.py`. Data model: `roadmaps`, `roadmap_days`.
