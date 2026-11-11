# 05 · Log in, log out and landing

**Week:** 5

## Why

Students come back every day, and the creator needs to reach the progress view (R2, R3). Screen 2 in `design.md`.

## Done when

- [ ] Screen 2 matches `design.md`, in all four states
- [ ] A correct email and password start a 7-day session; a wrong one shows *"Email or password is incorrect..."* and never says which was wrong
- [ ] After login, each user lands on the right screen per "Landing after login" in `screens.md`
- [ ] **Log out** appears on every page after login and ends the session
- [ ] A logged-out visitor opening any page except Sign up and Log in is sent to Log in
- [ ] Tests cover correct password, wrong password and logged-out access

## Touches

`app/routes/auth.py`, `app/rules/accounts.py`, `app/templates/login.html`, `app/templates/base.html`, `tests/test_login.py`. Data model: `users`.
