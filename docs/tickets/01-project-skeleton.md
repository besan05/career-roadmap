# 01 · Project skeleton

**Week:** 5

## Why

Every other ticket needs a running app, a database and a test runner. This one is deliberately boring: nothing a student sees, only the ground the rest stands on.

## Done when

- [ ] `flask run` starts the app and shows a placeholder page on the laptop
- [ ] `schema.sql` creates every table in `data-model.md`, with every field, including `project_goal`, `is_demo`, `consented_at` and `posting_attempts`
- [ ] The folders match `rules.md` section 3 (`app/routes`, `rules`, `data`, `ai`, `templates`, `static`, `cli.py`, `plans/`, `tests/fake_ai/`)
- [ ] `.env.example` lists every variable from `workflow.md`; `.gitignore` covers `.env` and `instance/`
- [ ] `pytest` runs and one test passes
- [ ] `requirements.txt` holds only the dependencies in `stack.md`

## Touches

`app/__init__.py`, `schema.sql`, `requirements.txt`, `.env.example`, `.gitignore`, `tests/test_smoke.py`. Data model: all tables (created, still empty).
