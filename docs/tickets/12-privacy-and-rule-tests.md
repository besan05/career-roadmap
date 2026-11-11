# 12 · Privacy and rule tests

**Week:** 6

## Why

Before real students sign up, the rules that protect them must be proven, not assumed (N1, N3, N5, N6). Must be done before invites go out.

## Done when

- [ ] Logged in as student A, typing the address of student B's roadmap, day or link shows nothing of B's (N1)
- [ ] A student typing the progress view address is refused (N5)
- [ ] No request can change or delete a submission, except `unlock` and `reset-demo` (N3, D56)
- [ ] The AI key does not appear in any page or browser request (N6)
- [ ] Every form rejects a request without its CSRF token
- [ ] All tests in `rules.md` section 10 exist and pass

## Touches

`tests/test_privacy.py`, `tests/test_rules.py`; fixes in `app/rules/` if a test fails. Data model: none.
