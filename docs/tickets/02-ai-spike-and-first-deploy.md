# 02 · AI spike and first deploy

**Week:** 5

## Why

The biggest unknown is whether the free host can reach the AI (A5). It is proven before any screen is built around it (D54, D55). The same work puts the skeleton live for the first time.

## Done when

- [ ] The skeleton from ticket 01 runs on PythonAnywhere at its public address
- [ ] A temporary page, only on the deployed app, sends one fixed question to Gemini and shows the answer
- [ ] The AI key comes from `.env` on PythonAnywhere and never appears in the code, the page or a commit (N6)
- [ ] If Gemini fails from PythonAnywhere, Groq is tried, then OpenRouter (D55)
- [ ] The provider and exact model that worked are recorded in `decisions.md`; if all fail, "templates only" is recorded and A5 marked failed
- [ ] The temporary page is removed before the ticket is closed

## Touches

`app/ai/client.py` (first version), PythonAnywhere web app settings, `decisions.md`. Data model: none.
