# Design

Every screen from [`screens.md`](screens.md), in words: what is on it, which requirement it serves, and its four states. The model reads this file next week, not the mockups.

**States used on every screen**

| State | Meaning here |
|---|---|
| Empty | The first time this user sees the screen, with nothing created yet |
| Loading | A request is on its way (pages are server-rendered, so this is mostly "a form was submitted") |
| Error | The request failed, or the input was refused |
| Full | Normal use, with data |

**Rule for all screens:** every field shown exists in [`data-model.md`](data-model.md) or is calculated from it (see "Derived values" there). No search, filters, avatars or settings.

---

## 4. Roadmap

**Serves:** R9, R10–R14b, N3, N4. **Who:** a student with a plan that is not finished.

### What is on it, top to bottom

| Part | Shows | Data |
|---|---|---|
| Header | App name, **Log out** | — |
| Top band | *"Your target · plan made from your job posting"* (or *"from the … template"*), the role in large type, e.g. *Junior AI Engineer* | `roadmaps.role_title`, `source`, `template_id` |
| Project goal | A lilac box inside the band: *"By day 10 you will have"* and one sentence, e.g. *"A deployed AI assistant that answers questions about any PDF and shows the sources it used."* | `roadmaps.project_goal` (D65) |
| Buttons | **View job posting** (posting plans only, opens a popup); **Choose a different plan** (only before day 1 is submitted) | `roadmaps.job_posting`; derived: no submission yet |
| Progress ring | A ring with *"3/10 days done"* in the middle | Derived: days completed |
| Journey line | 10 short bars labelled Day 1–10: filled for completed days, dark blue for today, white for locked | Derived per day |
| Today card (left, large) | **Today** label, "Day N · about 30 minutes", title, instructions, a *"What to submit"* box, link field, the shareable-link reminder, **Submit link** | `roadmap_days.title`, `instructions`, `expected_evidence` |
| "Your 10 days" list (right) | Completed days: tick, title, date (click opens instructions and the submitted link, read-only). Today: highlighted, with "Today". Locked: lock icon and title only | `roadmap_days.title`, active `submissions.url`, `submitted_at` |

Times are shown in Jordan time as `2026-11-18 21:14`.

### Four states

**Empty (day 1, nothing submitted).** Ring at *"0/10"*, all journey bars white except day 1. A green note above the Today card: *"Your plan is ready. Each day takes about 30 minutes and unlocks the next one when you submit a link to your work. Start with day 1 below."* Day 1 is open; days 2–10 are locked. **Choose a different plan** is visible. (A student with no plan never reaches this screen; they land on Choose your target.)

**Loading (after pressing Submit and confirming).** The link field and the button are disabled, and the button reads **Submitting…**, so it cannot be pressed twice. Nothing else on the page changes until the server answers.

**Error.** Three cases, each shown inside the current day box, above the link field. The typed link stays in the field.
- Not a valid `http`/`https` link: *"Please enter a valid link (e.g. https://...)."* Checked in the browser and again on the server. Nothing is saved.
- The save failed (server or connection): *"We couldn't save your link. Nothing was saved. Check your connection and press Submit again."*
- The day is no longer current (e.g. submitted in another tab): the page reloads at the real current day with *"This day was already submitted."*

If the whole page fails to load, the student sees the app's general error page: *"Something went wrong on our side. Try again in a minute."* with a **Try again** link. No stack trace (rules.md, section 8).

**Full (e.g. day 4).** Days 1–3 completed with times, day 4 open as **Today**, days 5–10 locked. **Choose a different plan** is gone. After a successful submit, the page reloads with the next day open; after day 10 it goes to Completion.

### What the model decided, and what I accepted

| Decided by the model | Accepted? |
|---|---|
| A "Today" label on the current day | Yes |
| A source line under the title | Yes: uses `source`, no new field |
| An intro line in the empty state | Yes |
| The "already submitted in another tab" error | Yes: N3 makes it possible |
| Completed days show the link directly instead of only on click | **No.** Kept collapsed, as screens.md says; opens on click |
| Blue and grey colours, plain list layout | **No.** Too plain. Tried seven looks on the canvas; chose "Sky & lilac" with a top band, ring and journey line (D67) |

**Fields not in data-model.md:** the project goal. The first design had no picture of where the 10 days lead, and that sentence was not stored anywhere. Added on purpose as `roadmaps.project_goal` (D65).

**Look (D67, "Sky & lilac"):** pale blue page, sky-blue top band, lilac goal box and Today label, blue buttons with white text, green ticks for completed days. Dark text on every background. Colour is never the only signal: completed days also have a tick, locked days a lock. Font: Nunito.

---

## 1. Sign up

**Serves:** R1, R1b. **Who:** an invited student with no account.

### What is on it

| Part | Shows | Data |
|---|---|---|
| Left band | *"10 days. 30 minutes a day. One real project."*, one line on how it works, and three numbered steps (paste a posting, one task a day, submit a link) | — |
| Form | *"Create your account"*: Email, Password (at least 8 characters), Invite code | `users.email`, `password_hash`; `invite_codes` |
| Consent box | *"We store your email, your plan, the job posting you paste, your links and when you submit them. Only you and the person running this test can see them. Everything is deleted when the test ends."* and an **I agree** checkbox | `users.consented_at` |
| Actions | **Sign up**; *"Already have an account? Log in"* | — |

### Four states

**Empty.** All fields empty, box unticked.

**Full.** Fields filled, box ticked, **Sign up** active.

**Loading.** Fields and the button are disabled; the button reads **Creating your account…**.

**Error.** Each problem is shown under its own field with a red border; what the student typed stays (except the password field is not refilled after a server error). Messages:
- Invite code missing or wrong: *"This invite code doesn't exist. Check it with the person who invited you."*
- Invite code used: *"This invite code has already been used. Ask the person who invited you for a new one."*
- Email already has an account: *"This email already has an account. Log in instead."*
- Password too short: *"Use at least 8 characters."*
- Box not ticked: *"Tick \"I agree\" to continue."*

**Decided by the model, accepted:** the left band with the three steps; listing the stored data in the consent box exactly as R1b says.

## 2. Log in

**Serves:** R2, R3. **Who:** students and the creator.

### What is on it

| Part | Shows | Data |
|---|---|---|
| Left band | *"Welcome back"*, *"Your plan is waiting where you left it."*, and a lilac note: *"No dates, no deadlines. Each day opens when you submit the one before it."* | — |
| Form | Email, Password, **Log in**; *"Have an invite code? Sign up"* | `users.email`, `password_hash`, `role` |

### Four states

**Empty.** Both fields empty.

**Full.** Both filled, **Log in** active.

**Loading.** Fields and button disabled; the button reads **Logging in…**.

**Error.** A red box above the fields: *"Email or password is incorrect. If you forgot your password, ask the person who invited you."* The email stays; the password field is cleared. The message never says which of the two was wrong.

**After:** lands per "Landing after login" in screens.md. The creator lands on the Progress view.

**Decided by the model, accepted:** the "no dates, no deadlines" note, because it explains R13 before the student sees the Roadmap.

## 3. Choose your target

**Serves:** R4–R9, R5b, R7, R8. **Who:** a student with no plan (first login, or after "Choose a different plan" before day 1).

### What is on it, top to bottom

| Part | Shows | Data |
|---|---|---|
| Header | App name, **Log out** | — |
| Top band | *"Let's build your plan"* and one line: *"Paste a real job posting and get 10 daily tasks of about 30 minutes, all aimed at one project you can show."* | — |
| Posting card (main option) | A **Recommended** label, *"Paste a job posting"*, a large text box, *"3 of 3 posting tries left"*, a character counter *"1,240 / 6,000 characters"*, **Create my plan** | Tries: derived from `users.posting_attempts` (3 minus it). Counter: counted in the browser, checked again on the server |
| Divider | *"or pick a ready-made role"* | — |
| Template cards | One card per template: icon, title, the one-line description, *"10 days · about 30 minutes a day"*, **Use this plan** | `plans/*.json`: `role_title`, `description` |

### Four states

**Empty (nothing typed yet).** Text box empty with its placeholder, counter at 0, *"3 of 3 posting tries left"*, both templates shown.

**Full (posting pasted, ready to send).** The posting fills the box, the counter shows its length, **Create my plan** is active.

**Loading (after pressing Create my plan).** The text box, the main button and both **Use this plan** buttons are disabled, so nothing can be sent twice. The button reads **Building your plan…**, and a box under the counter says: *"Building your 10-day plan. This takes up to a minute. Please keep this page open."* On success the Roadmap opens (Empty state, day 1).

**Error.** The pasted text always stays in the box. Each case shows one message, above the button:
- The AI failed twice, timed out or is unavailable (R7): *"We couldn't build a plan from this posting right now. Your tries were not used. Pick a role below to start today, or try again in a few minutes."* The divider changes to *"Start now with a ready-made role"* and the template cards get a stronger border. Tries stay the same (D57).
- Not an IT job posting (R5b): *"This doesn't look like an IT job posting. Paste a different one or pick a role below."* This uses a try.
- Empty box: *"Paste the job posting first."* Nothing is sent.
- Over 6,000 characters: *"This posting is too long. Paste only the job description part."* Nothing is sent.
- All 3 tries used (R5): the posting card is replaced by *"You've used all 3 posting tries. Pick a role below to start."*

### What the model decided, and what I accepted

| Decided by the model | Accepted? |
|---|---|
| A "Recommended" label on the posting option | Yes: the posting is the main difference from roadmap.sh |
| Showing "3 of 3 posting tries left" before the first try | Yes: students should know the limit before they use it |
| Disabling the template buttons while the AI works | Yes: avoids a template and an AI plan being created at the same time |
| Saying "Your tries were not used" in the error | Yes: matches D57 and stops students from worrying |
| A third template, Junior AI Engineer | **Not now.** R8 asks for two; a third is one more 10-day plan to write. Can be added later as one JSON file |

**Fields not in data-model.md:** none. Tries left come from `posting_attempts`.

**Look:** same as the Roadmap screen (D67).

## 5. Completion

**Serves:** R15, N2. **Who:** a student who has submitted day 10.

### What is on it

| Part | Shows | Data |
|---|---|---|
| Top band | A large green tick, *"You finished all 10 days"*, *"You've built 10 days of real evidence for your portfolio, one link at a time."*, and all 10 journey bars filled | Derived: finished |
| What you built | A lilac box: *"What you built · Junior AI Engineer"* and the project goal | `roadmaps.role_title`, `project_goal` |
| Three numbers | Started, Finished, Days taken | `started_at`; first `submitted_at` of day 10; the difference |
| What happens next | *"The person running this test will open your final link and review your project."* and **View my roadmap** (opens the Roadmap read-only) | — |

### Four states

**Full.** As above.

**Empty.** Does not apply: a student only reaches this screen after day 10, so there is always data.

**Loading.** Does not apply: the page is built on the server and has no buttons that send anything.

**Error.** If the page cannot load: the app's general error page, *"Something went wrong on our side. Your work is safe. Try again in a minute."* with **Try again**.

**N2 check:** nothing on this screen mentions jobs, interviews or hiring.

**Decided by the model, accepted:** showing Started, Finished and Days taken (all calculated, no new field); the "What happens next" line. **Not added:** showing whether the work has been reviewed. R15 does not ask for it.

## 6. Progress view

**Serves:** R16–R18, N1, N5. **Who:** the creator only.

### What is on it

| Part | Shows | Data |
|---|---|---|
| Header | App name, a **Creator** label, **Log out** | `users.role` |
| Title | *"Test progress"* and *"Read only. Unlocking a day, marking reviewed and invite codes are scripts."* | — |
| Four numbers | Signed up, Started a plan, Finished 10 days, Reviewed. The Demo Student is not counted | Derived from `users`, `roadmaps`, `submissions`; `is_demo` excluded |
| Table | One row per student: email (Demo Student labelled **Demo**), plan (template name or "From posting" or "No plan yet"), started, current day with a small bar, last link time, days since start, reviewed Yes/No | `users.email`, `is_demo`, `roadmaps.*`, `submissions.submitted_at` |
| Expanded row | Clicking a row opens its evidence links (day, link, time) and, for posting plans, **Open the pasted job posting** | `submissions.url`, `submitted_at`, `roadmaps.job_posting` |

The table scrolls sideways on narrow screens instead of squeezing.

### Four states

**Empty (no one has signed up yet).** *"No students yet. Create invite codes with `flask create-invite`, then send one to each tester. Students show up here as soon as they sign up."*

**Full.** As above, e.g. six rows: one finished and reviewed, three in progress, one with no plan, and the Demo Student.

**Loading.** Does not apply: the page is built on the server and has no actions.

**Error.** A red box: *"Couldn't load the progress table. Nothing was changed. Reload the page; if it keeps failing, check the server log on PythonAnywhere."*

**Decided by the model, accepted:** the four summary numbers (calculated, no new field); the Demo label; one row open at a time. **Not added:** buttons for unlock or review. They stay scripts (D26).
