# Agents

Which model does which job, and how I hand work to it.

| Job | Model | Why |
|---|---|---|
| Small ticket (one file, clear Done when) | A fast model | Cheap and quick; little can go wrong |
| Normal ticket | A strong model | Needs to hold the plan, the rules and several files at once |
| Risky ticket (data, secrets, deploy, the AI call) | A strong model, and I read its plan before any code | Mistakes here are expensive or public |
| Review of a pull request | A strong model in a **fresh chat** | It has not seen the code being written, so it is not grading its own work |

## How every ticket runs

1. A new branch, then a **new chat** for every ticket, so the model only sees what this ticket needs (and a short chat costs fewer tokens).
2. I give it four things: `plan.md`, the one ticket, `rules.md` + `workflow.md`, and the files the ticket touches (plus `data-model.md` or `design.md` when needed).
3. It gives a plan first. No code until I have answered its questions.
4. It writes the code and lists every file it created or changed, and why.
5. I run the tests, commit with the ticket title, push and open a pull request.
6. I review the pull request on GitHub as a stranger, and ask: "Is there anything in this diff that the ticket did not ask for?" I send something back when it is wrong, then merge and delete the branch.
