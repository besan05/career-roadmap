# 04 · Sign up with invite code and consent

**Week:** 5

## Why

Students need an account before anything else (R1, R1b). Screen 1 in `design.md`.

## Done when

- [ ] Screen 1 matches `design.md`, in all four states
- [ ] Sign-up is refused, with the message from `design.md`, for: no code, wrong code, used code, an email that already has an account (any letter case), a password under 8 characters, and the box not ticked
- [ ] On success, in one step: the account is created with `consented_at`, the password is hashed, the code is marked used
- [ ] The email is stored in lowercase
- [ ] After sign-up the student lands on Choose your target
- [ ] Every refusal case above has a test

## Touches

`app/routes/auth.py`, `app/rules/accounts.py`, `app/templates/signup.html`, `app/static/style.css`, `tests/test_signup.py`. Data model: `users`, `invite_codes`.
