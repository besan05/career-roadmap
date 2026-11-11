# 09 · Completion screen

**Week:** 6

## Why

Students need to see that they finished, without any promise of a job (R15, N2). Screen 5 in `design.md`.

## Done when

- [ ] Screen 5 matches `design.md`: tick, *"You finished all 10 days"*, what you built, Started / Finished / Days taken, "What happens next"
- [ ] It opens after day 10 is submitted and cannot be reached before
- [ ] **View my roadmap** opens the Roadmap in read-only mode
- [ ] No word on the screen promises or hints at a job or interview (N2)
- [ ] The general error page from `design.md` exists and is used on every screen

## Touches

`app/routes/roadmap.py`, `app/templates/completion.html`, `app/templates/error.html`, `tests/test_completion.py`. Data model: read only.
