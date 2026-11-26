# 02 · AI spike and first deploy

**Week:** 5

## Why

The biggest unknown is whether the free host can reach the AI (A5). It is proven before any screen is built around it (D54, D55). The same work puts the skeleton live for the first time.

## Done when

- [x] The skeleton from ticket 01 runs on PythonAnywhere at its public address
- [x] A temporary page, only on the deployed app, sends one fixed question to Gemini and shows the answer
- [x] Both AI keys come from `.env` on PythonAnywhere and never appear in the code, the page or a commit (N6)
- [x] The same page also sends the question once to the backup through Groq, and shows that answer too (D69)
- [x] If Gemini fails from PythonAnywhere, Groq becomes the main model; if both fail, OpenRouter is tried (D55)
- [x] The providers and exact models that worked (Gemini and the Groq backup) are recorded in `decisions.md`; if all fail, "templates only" is recorded and A5 marked failed
- [x] The temporary page is removed before the ticket is closed

## Touches

`app/ai/client.py` (first version), PythonAnywhere web app settings, `decisions.md`. Data model: none.

## Result (2026-11-25)

Live at https://besan05.pythonanywhere.com. Gemini `gemini-3.5-flash-lite` answered in 0.9 s; `gemini-3.5-flash` timed out at 30 s. Groq `openai/gpt-oss-120b` answered in 0.4 to 0.6 s. A5 passed. See D70 to D74. The spike page was never merged into main (D72).
