# 13 · Creator progress view

**Week:** 7

## Why

I need to see who is moving and who stopped, without touching the database by hand (R16). Screen 6 in `design.md`.

## Done when

- [ ] Screen 6 matches `design.md`, in the Empty, Full and Error states
- [ ] The four numbers and every row match what is stored; the Demo Student is labelled and not counted
- [ ] Clicking a row shows its evidence links with times and, for posting plans, the pasted posting
- [ ] The page has no buttons that change anything
- [ ] Only the creator can open it (tested in ticket 12)

## Touches

`app/routes/creator.py`, `app/rules/progress.py`, `app/templates/progress.html`, `tests/test_progress.py`. Data model: read only.
