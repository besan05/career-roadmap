# 11 · Choose a different plan before day 1

**Week:** 6

## Why

A student who picked the wrong role should not be stuck, but submitted work must never be deleted (R9, D39).

## Done when

- [ ] **Choose a different plan** deletes the roadmap and its days and opens Choose your target
- [ ] It is refused by the server once any submission exists
- [ ] `posting_attempts` is not reset
- [ ] Tests cover before day 1 (allowed) and after day 1 (refused)

## Touches

`app/routes/plan.py`, `app/rules/plans.py`, `tests/test_choose_again.py`. Data model: `roadmaps`, `roadmap_days` (delete, only with no submissions).
