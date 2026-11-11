# 07 · Roadmap screen

**Week:** 6

## Why

The screen students open every day (R10, R13, R14, R14b). Screen 4 in `design.md`.

## Done when

- [ ] Screen 4 matches `design.md`: top band with role, project goal, progress ring and journey line; Today card; "Your 10 days" list
- [ ] The Empty and Full states match `design.md`
- [ ] Completed days open read-only with their instructions and submitted link; locked days cannot be opened by clicking or by typing their address
- [ ] **View job posting** opens the pasted posting for posting plans and is hidden for template plans
- [ ] **Choose a different plan** shows only before day 1 is submitted (the action itself is ticket 11)
- [ ] A student who returns after a week lands on the same day

## Touches

`app/routes/roadmap.py`, `app/rules/days.py`, `app/templates/roadmap.html`, `app/static/style.css`, `app/static/app.js` (posting popup). Data model: read only.
