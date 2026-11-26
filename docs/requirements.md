# Requirements

What the MVP must do and must never do. Every item fits inside [`scope.md`](scope.md).

## Users

| User | Who | How many |
|---|---|---|
| **Student** | A final-year or newly graduated IT student I invite | 5 during the test |
| **Creator** | Me: builds the app, manages invites, reviews work | 1 |
| **Demo Student** | An account used only on Demo Night and in rehearsals | 1, excluded from all measurement |

## Must do

### Access

**R1 Invite-only sign-up.** A student creates an account with email, password and an invite code I issued. Each code works once and does not expire. Emails are compared without case. Passwords have at least 8 characters.
Done when: sign-up with no code, a wrong code, an already-used code, an email that already has an account (in any letter case), or a password under 8 characters is refused with a message.

**R1b Consent.** The sign-up screen says what is stored (email, plan, the pasted posting, links, submission times), who sees it (only the student and the creator), and that it is deleted when the test ends. The student must tick "I agree" to sign up, and the time they agreed is stored.
Done when: sign-up without ticking the box is refused with a message; a new account has its consent time stored.

**R2 Log in and out.** A student logs in with email and password and stays logged in for 7 days or until they log out.
Done when: a student can log in, close the browser, come back and still see their plan; after logging out, the plan page sends them to the login page.

**R3 Creator login.** I log in through the same login page with an account marked as creator, which opens the creator view.
Done when: logging in as the creator opens the progress view; logging in as a student never does.

### Getting a plan

**R4 Choose a target.** On first login, a student either pastes a job description or picks a role template. There is no skill-level rating.
Done when: a new student cannot reach day 1 without doing one of the two.

**R5 AI plan from a job description.** When a student pastes a job description, the app sends only the posting text to the AI model and shows the generated 10-day plan on the same visit. A posting may be up to 6,000 characters. A student can create a plan from a posting up to 3 times before day 1; after that, only templates are offered. An attempt counts only when the AI answers (with a plan, a broken plan, or a refusal). The automatic retry, timeouts, outages and rate limits do not count.
Done when: pasting a real posting shows a 10-day plan within about a minute, with no action from the creator; a posting over 6,000 characters is refused with a message; with the AI key switched off, failed tries leave the attempts unchanged; after 3 counted attempts, only the templates are shown.

**R5b Not an IT job posting.** The AI may refuse a text that is not an IT job posting. The student then sees: *"This doesn't look like an IT job posting. Paste a different one or pick a role below."* No plan is saved.
Done when: pasting "hello" or a nursing job posting shows the message and saves no plan.

**R6 Plan check.** Before saving, the app checks the AI's plan: a role title, a project goal (one sentence on what the student will have built by day 10), and exactly 10 days in order, each with a title, task instructions for about 30 minutes, and a description of the evidence expected. If the check fails, it asks the AI once more.
Done when: a deliberately broken response (9 days, a missing field, no role title or no project goal) is never shown to the student.

**R6b Plan content.** The instructions sent to the AI (`app/ai/prompt.txt`) ask for: one project sized for 10 × 30 minutes; day 1 sets up a public repository; tasks point to existing free lessons instead of teaching from scratch; the expected evidence of every day is something that can be linked. The code checks only the structure (R6); content is checked by me reading sample plans.
Done when: `prompt.txt` asks for all four, and three plans made from real postings meet them when I read them (A4).

**R7 Backup AI, then fallback.** If Gemini fails twice (a broken plan, a timeout or an error), the app sends the same posting and instructions once to the backup model through Groq (D70), and applies the same check (R6). If that also fails, or both services are unavailable, the student sees a short message ("try again in a few minutes; your tries were not used") and the role templates.
Done when: with the Gemini key switched off, a posting still gets a plan from the backup; with both keys switched off, the message and the template list appear, not an error page.

**R8 Role templates.** The app ships with pre-written 10-day plans, at least *Junior Frontend Developer* and *Junior Data Analyst*. Picking one loads it immediately.
Done when: picking each template shows its 10-day plan without any AI call.

**R9 One plan per student.** Before submitting day 1, a student can discard their plan and choose again. After day 1, the plan is fixed.
Done when: the "choose again" option disappears once day 1 is submitted.

### Daily execution

**R10 One day at a time.** The student sees their current day and all completed days. Future days are visible as locked but cannot be opened.
Done when: a locked day cannot be opened by clicking it or by typing its address.

**R11 Evidence to complete.** A day is completed only by submitting one link. The app accepts it only if it is a valid `http` or `https` URL.
Done when: `abc` and `ftp://example.com` are refused; `https://github.com/user/repo` is accepted.

**R12 Unlock on submit.** Submitting a valid link completes the day and unlocks the next one immediately.
Done when: after a valid submission, the next day opens without the creator doing anything.

**R13 Sequence, not calendar.** Days have no dates or deadlines. If a student stops, the app waits; when they return, they resume at their current day.
Done when: a student who logs in again after a week lands on the same day they left.

**R14 Shareable links.** The submit screen reminds the student that the link must be viewable by the creator (for example, a Google Drive link shared with view access).
Done when: the reminder is visible on every submit screen.

**R14b View the posting.** For a plan made from a posting, the Roadmap screen has a button that shows the pasted posting.
Done when: the button opens the posting for posting-based plans and does not appear for template plans.

### Completion

**R15 Completion screen.** After day 10 is submitted, the student sees a screen confirming all 10 steps are submitted.
Done when: the screen appears after day 10 and cannot be reached before it.

### Creator

**R16 Progress view.** A read-only page, reachable only by me, lists each student with: email, target role or "from posting", start time, current day, every evidence link with its submission time, and review status. The Demo Student is marked as such.
Done when: every student appears, and their current day and links match what is stored.

**R17 Unlock a mistake.** I can unlock a submitted day so the student can resubmit (with a script).
Done when: after unlocking, the student can resubmit that day and only that day.

**R18 Mark as reviewed.** I mark a student as reviewed when their final link (1) opens without asking for access, (2) contains work that matches the plan's project, and (3) has a README explaining it (with a script).
Done when: the status shows as reviewed in the progress view.

## Must never do

**N1 Privacy.** Never show one student's progress, evidence or identity to another student.
Done when: logged in as student A, typing the address of student B's plan or evidence shows nothing of B's.

**N2 No false promises.** Never promise, guarantee or imply that finishing leads to a job offer or an interview. Outcome wording says it builds skills and evidence of work.
Done when: a read-through of every screen finds no promise of a job or interview.

**N3 No skipping or editing.** Never accept evidence for a locked day, or a change to evidence on a completed day. Only the creator can unlock one. The only change ever made to a saved submission is `unlock` setting its `replaced_at`, once. The only data ever deleted after day 1 is the Demo Student's, by the `reset-demo` script (D51).
Done when: such a request is refused by the server, even when sent directly and not through the page.

**N4 Honest timestamps.** Never let the student set the time of a submission. The server records it.
Done when: changing the clock on the student's computer does not change the stored submission time.

**N5 No access beyond your own.** Never let a student reach the creator view, even by typing its address.
Done when: a student typing the creator view address is refused.

**N6 The AI key stays on the server.** Never send the AI key to the browser.
Done when: the key does not appear in the page source or in any request the browser makes.

**N7 Nothing personal to the AI.** Never send a student's email, name or progress to the AI model. Only the posting text and fixed instructions are sent.
Done when: the request sent to the AI contains only the posting and the instructions.

## Quality

| Area | Requirement | Done when |
|---|---|---|
| Device | Desktop browser first. Phones are not optimised. | Every screen works on a laptop screen without sideways scrolling. |
| Language | English only. | No other language appears in the interface. |
| Cost | Zero cost. The AI runs on Gemini's free tier, no billing attached. | No service used by the app has a payment method attached. |
| Storage | Text only: links, plans, progress. No file uploads. | The app has no file-upload field anywhere. |
| Demo | Runs live on Demo Night, starting from Log in as the Demo Student. | Log in, paste a posting, get a plan, submit day 1, then run `reset-demo`: works three times in a row on the demo laptop. |

## Measurement

Supports section 4 of [`brief.md`](brief.md). The Demo Student is excluded from every number.

- **Invited:** 5 students.
- **Completed:** all 10 days submitted within **10 days** of the student's start time, and marked reviewed by the creator.
- **Success:** at least **3** students complete.
- **Recorded automatically:** start time, every submission time, current day. From these: completions, days taken, and the day each dropout stopped.

## Open questions

1. **Accountability without nudges.** The brief says students quit when nobody asks "where are you?", but the app waits quietly, and I do not nudge testers during the test (D62). A "you've been away X days" message on return is the cheapest fix if testers stall, but only after the test, so it does not spoil A1.
2. **The AI prompt wording.** What it must ask for is fixed in R6b. The exact wording is written in the week-3 spike and refined in week 5.
