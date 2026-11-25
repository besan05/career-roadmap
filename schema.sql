-- Career Roadmap database. Tables and fields from docs/data-model.md.
-- Created once with: flask init-db
--
-- Timestamps are ISO 8601 text in UTC, always set by the server in Python.
-- Yes/no fields are INTEGER 0 (no) or 1 (yes).
-- Foreign keys are enforced because app/data/db.py turns them on.
-- No ON DELETE CASCADE: every delete is written out explicitly in code,
-- so a delete can never quietly remove a student's submissions (N3).

-- Students, the Demo Student and the creator.
CREATE TABLE users (
    id               INTEGER PRIMARY KEY,
    -- R1: emails are stored and compared in lowercase
    email            TEXT    NOT NULL UNIQUE CHECK (email = lower(email)),
    password_hash    TEXT    NOT NULL,
    -- N5: only a creator can open the progress view
    role             TEXT    NOT NULL CHECK (role IN ('student', 'creator')),
    -- D51: yes only for the Demo Student, who is left out of measurement
    is_demo          INTEGER NOT NULL DEFAULT 0 CHECK (is_demo IN (0, 1)),
    consented_at     TEXT,
    -- R5: counted only when the AI answered, at most 3
    posting_attempts INTEGER NOT NULL DEFAULT 0
                     CHECK (posting_attempts BETWEEN 0 AND 3),
    created_at       TEXT    NOT NULL,
    -- R1b: every account except the creator has ticked "I agree"
    CHECK (role = 'creator' OR consented_at IS NOT NULL)
);

-- Single-use codes that allow a student to sign up (R1). They do not expire.
CREATE TABLE invite_codes (
    id         INTEGER PRIMARY KEY,
    -- The real code is printed once and never stored
    code_hash  TEXT    NOT NULL UNIQUE,
    created_at TEXT    NOT NULL,
    -- R1: one code makes one account. Empty = unused
    used_by    INTEGER UNIQUE REFERENCES users (id),
    used_at    TEXT
);

-- One student's plan. A student has at most one.
CREATE TABLE roadmaps (
    id           INTEGER PRIMARY KEY,
    user_id      INTEGER NOT NULL UNIQUE REFERENCES users (id),
    source       TEXT    NOT NULL CHECK (source IN ('template', 'posting')),
    -- e.g. junior-frontend. Empty for posting-based plans
    template_id  TEXT,
    role_title   TEXT    NOT NULL,
    -- D65: what the student will have built by day 10
    project_goal TEXT    NOT NULL,
    -- Posting-based plans only, as pasted
    job_posting  TEXT,
    started_at   TEXT    NOT NULL,
    -- R18: empty = not reviewed. Set by the creator
    reviewed_at  TEXT
);

-- The 10 steps of one roadmap.
CREATE TABLE roadmap_days (
    id                INTEGER PRIMARY KEY,
    roadmap_id        INTEGER NOT NULL REFERENCES roadmaps (id),
    -- R6: exactly 10 days, numbered 1 to 10
    day_number        INTEGER NOT NULL CHECK (day_number BETWEEN 1 AND 10),
    title             TEXT    NOT NULL,
    instructions      TEXT    NOT NULL,
    expected_evidence TEXT    NOT NULL,
    UNIQUE (roadmap_id, day_number)
);

-- Evidence links. Never deleted or edited (N3, N4).
CREATE TABLE submissions (
    id             INTEGER PRIMARY KEY,
    roadmap_day_id INTEGER NOT NULL REFERENCES roadmap_days (id),
    url            TEXT    NOT NULL,
    -- N4: set by the server, never by the student
    submitted_at   TEXT    NOT NULL,
    -- R17: empty = active. Set once by unlock, the only change ever made
    replaced_at    TEXT
);

-- N3: each day has at most one active submission
CREATE UNIQUE INDEX one_active_submission_per_day
    ON submissions (roadmap_day_id)
    WHERE replaced_at IS NULL;
