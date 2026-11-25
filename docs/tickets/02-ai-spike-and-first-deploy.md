# 02 · AI spike and first deploy

**Week:** 5

## Why

The biggest unknown is whether the free host can reach the AI (A5). It is proven before any screen is built around it (D54, D55). The same work puts the skeleton live for the first time.

## Done when

- [ ] The skeleton from ticket 01 runs on PythonAnywhere at its public address
- [ ] A temporary page, only on the deployed app, sends one fixed question to Gemini and shows the answer
- [ ] Both AI keys come from `.env` on PythonAnywhere and never appears in the code, the page or a commit (N6)
- [ ] The same page also sends the question once to the backup, Llama through Groq, and shows that answer too (D69)
- [ ] If Gemini fails from PythonAnywhere, Groq becomes the main model; if both fail, OpenRouter is tried (D55)
- [ ] The providers and exact models that worked (Gemini and Llama) are recorded in `decisions.md`; if all fail, "templates only" is recorded and A5 marked failed
- [ ] The temporary page is removed before the ticket is closed

## Touches

`app/ai/client.py` (first version), PythonAnywhere web app settings, `decisions.md`. Data model: none.
