# 08 · Submit a link and unlock the next day

**Week:** 6

## Why

The core of the product: a day counts only when the student shows their work (R11, R12, N3, N4).

## Done when

- [ ] Only a valid `http` or `https` link is accepted, checked in the browser and again on the server; `abc` and `ftp://example.com` are refused
- [ ] A confirmation step comes before saving: *"Once submitted, this cannot be edited. Submit?"*
- [ ] The Loading and Error states match `design.md`, including "already submitted in another tab"
- [ ] The submission time comes from the server; changing the computer clock changes nothing
- [ ] Saving a link opens the next day immediately; after day 10 the student goes to Completion
- [ ] A link for a locked day or a completed day is refused by the server even when sent directly
- [ ] Tests cover a valid link, an invalid link, a locked day and a completed day

## Touches

`app/routes/roadmap.py`, `app/rules/days.py`, `app/rules/links.py`, `app/data/submissions.py`, `app/templates/roadmap.html`, `tests/test_submit.py`. Data model: `submissions`.
