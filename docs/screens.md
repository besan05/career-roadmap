# Screens

Every screen in the MVP. Desktop browser, English only. Each screen traces back to [`requirements.md`](requirements.md).

## The six screens

| # | Screen | Who | What happens there | Requirements |
|---|---|---|---|---|
| 1 | Sign up | Student | Creates an account with an invite code and consent | R1, R1b |
| 2 | Log in | Student, creator | Enters the app | R2, R3 |
| 3 | Choose your target | Student, until day 1 | Pastes a job posting or picks a template; gets a plan | R4–R9, R5b |
| 4 | Roadmap | Student | Works through the 14 days, one link per day | R9–R14b, N3, N4 |
| 5 | Completion | Student | Sees that all 14 days are submitted | R15, N2 |
| 6 | Progress view | Creator | Sees every student's progress and links | R16–R18, N1, N5 |

**Not building:** a landing page, password reset, profile or settings pages, notifications, a mobile layout, an admin screen for codes, unlocking or reviewing (done with scripts), and any screen showing other students.

## Map

```
 1 Sign up ──▶ 2 Log in
                  │
     ┌────────────┼──────────────┬──────────────┐
  no plan     plan in        all 14 done      creator
     │        progress            │              │
     ▼            ▼               ▼              ▼
 3 Choose ──▶ 4 Roadmap ◀──── 5 Completion   6 Progress
   target   ◀── choose again       (read-only roadmap)
             (before day 1 only)
```

## Landing after login

| Who | Lands on |
|---|---|
| Student with no plan | 3 Choose your target |
| Student with a plan in progress | 4 Roadmap |
| Student who submitted all 14 days | 5 Completion |
| Creator | 6 Progress view |

---

## 1. Sign up

**Shows:** app name, one line on what it does, fields for email, password (at least 8 characters) and invite code, a short note on what is stored (email, plan, the pasted posting, links, submission times), who sees it (only you and the creator) and that it is deleted when the test ends, an **I agree** checkbox, a **Sign up** button, and a link to **Log in**.

**Errors** (shown under the field): missing, wrong or already-used invite code; an email that already has an account; a password under 8 characters; the box not ticked.

**After:** → **3 Choose your target**.

## 2. Log in

**Shows:** email and password fields, a **Log in** button, and a link to **Sign up**.

**Errors:** wrong email or password → *"Email or password is incorrect. If you forgot your password, ask the person who invited you."*

**After:** lands per the table above.

## 3. Choose your target

**Shows two options:**
- **Paste a job posting** (main option): a large text box, a character counter (up to 6,000), and a **Create my plan** button.
- **Or pick a role**: the templates (at least Junior Frontend Developer and Junior Data Analyst), each with the one-line description from its file.

**While the AI works:** a loading message, e.g. *"Building your 14-day plan. This takes up to a minute."* The button is disabled so it cannot be pressed twice.

**If the AI fails twice, times out or is unavailable (R7):** *"We couldn't build a plan from this posting right now. Pick a role below to start."* The templates stay on screen.

**If the AI says it is not an IT job posting (R5b):** *"This doesn't look like an IT job posting. Paste a different one or pick a role below."*

**After 3 counted posting attempts (R5):** the posting box is replaced by *"You've used all 3 posting attempts. Pick a role below to start."*

**Errors:** empty text box → *"Paste the job posting first."* Over 6,000 characters → *"This posting is too long. Paste only the job description part."*

**After:** a plan is created → **4 Roadmap**.

## 4. Roadmap

The screen students use every day.

**Top:**
- Target role, from the template or from the AI.
- *"Day X of 14 completed"* and a progress bar.
- For posting-based plans: a **View job posting** button that opens the pasted posting in a popup (R14b).
- Before day 1 is submitted only: a **Choose a different plan** link (R9) → **3 Choose your target**.

**The 14 days**, each in one of three states:

| State | Looks like | Can do |
|---|---|---|
| Completed | Tick, title, submission time | Open to read instructions and the submitted link (read-only) |
| Current | Open by default | Read instructions and expected evidence, submit a link |
| Locked | Greyed out, lock icon, title only | Nothing |

**Current day:** title, the ~30-minute task, what evidence is expected, a link field, a **Submit** button, and the reminder: *"Make sure the link is viewable by your reviewer (e.g. Google Drive shared with view access)."*

**Submitting:**
1. Not a valid `http`/`https` link → *"Please enter a valid link (e.g. https://...)."* Nothing is saved.
2. Valid → *"Once submitted, this cannot be edited. Submit?"* with **Submit** and **Cancel**.
3. Confirmed → the day is completed with the server's time, and the next day opens. After day 14 → **5 Completion**.

**Read-only mode:** after completion, the same screen with no current day and no link field.

**Never on this screen:** points, badges, streaks, other students' data.

## 5. Completion

**Shows:** a message confirming all 14 days are submitted, worded within N2, e.g. *"You've built 14 days of real evidence for your portfolio."* Nothing about getting hired. A **View my roadmap** button → **4 Roadmap** in read-only mode.

## 6. Progress view

**Creator only.** One read-only table, one row per student:

| Column | Example |
|---|---|
| Student | student@example.com (the Demo Student is labelled "Demo") |
| Plan | Junior Frontend Developer (template) / From posting |
| Started | 2026-11-10 14:02 |
| Current day | 6 of 14 |
| Last submission | 2026-11-15 21:40 |
| Days since start | 5 |
| Reviewed | Yes / No |

Each row expands to show the 14 days: the evidence link (clickable) and its submission time. For posting-based plans, the pasted posting can be opened too.

**No actions in the app.** Invite codes, password resets, unlocking a day and marking reviewed are scripts (see `architecture.md`).

---

## On every screen after login

- A **Log out** button.
- No navigation menu: each user has one main screen.

## Open questions

1. **Welcome-back message.** If testers stall, add a line on screen 4 like *"You've been away X days. Day X is waiting."* (requirements, open question 1).
