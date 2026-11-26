# Tools

What the coding model may do on its own, what it must ask about first, and what it never does.

## May
- Read the repo and the files I give it.
- Run the tests.
- Run the app locally with fake AI answers (`AI_MODE=fake`).

## Ask first
- Install or add any package.
- Change anything in `docs/`. It tells me the change and I make it myself.
- Delete a file.
- Touch `.env`, or anything with a key in it.

## Never
- Push to `main`, or merge its own pull request.
- Run anything against production.
- See, ask for or print a real key or password. Secrets stay in `.env`, which is never committed (workflow.md).
