# 03 · Creator, invite and demo scripts

**Week:** 5

## Why

No one can sign up or log in until the creator account and invite codes exist. These are command-line scripts, not screens (D26, D49).

## Done when

- [x] `flask create-creator <email>` creates the creator account and prints a password once; it refuses if a creator exists
- [x] `flask create-invite` creates a single-use code, stores only its hash, and prints the code once
- [x] `flask create-demo <email>` creates the Demo Student with `is_demo = yes` and prints a password once; it refuses if one exists
- [x] Passwords and codes are never stored or logged in plain text
- [x] Each script has a test, using a test database

## Touches

`app/cli.py`, `app/data/users.py`, `app/data/invites.py`, `tests/test_cli.py`. Data model: `users`, `invite_codes`.
