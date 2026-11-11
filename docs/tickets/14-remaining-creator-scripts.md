# 14 · Unlock, review, password and demo scripts

**Week:** 7

## Why

The creator actions needed during the test and on Demo Night (R17, R18, D38, D51).

## Done when

- [ ] `flask unlock <email> <day>` sets `replaced_at` on that day's active link, once; the student can resubmit that day only
- [ ] `flask mark-reviewed <email>` sets `reviewed_at`, and refuses if 10 days are not complete
- [ ] `flask reset-password <email>` sets a temporary password and prints it once
- [ ] `flask reset-demo` deletes only the Demo Student's plan and links and resets their tries; it refuses any other user
- [ ] Each script checks its input before writing and has a test

## Touches

`app/cli.py`, `app/data/*.py`, `tests/test_cli.py`. Data model: `submissions.replaced_at`, `roadmaps.reviewed_at`, `users.password_hash`, Demo Student rows.
