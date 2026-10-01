# Example — Backlog file (fictional, for structure only)

Part of one worked example shared across this library: **Meterstream**, an imaginary internal
pipeline that ingests usage events and publishes daily summary reports.

This shows a **whole file** — items in several states at once, including one carried across a
phase boundary. The single-item format spec lives in `SKILL.md`; this shows how the file reads
once it has history in it. Note the `Status:` line: `<keyword> — <short note>`, where the first
word is always one of the six keywords and the note is optional.

---

```yaml
---
id: "reporting-backlog"
schema_version: 1
type: "backlog"
title: "Reporting — deferred work"
summary: "Open and deferred items for the reporting stage."
created_at: "2026-01-12T10:00:00+00:00"
updated_at: "2026-03-09T15:30:00+00:00"
status: "active"
project: "Meterstream"
initiative: "Phase 2"
next_item_id: "R12"
companion_docs:
  - "empty-report-handling"
---
```

# Reporting — deferred work

### R4 — Empty result set crashes the summary step

- **Status:** done — stated-empty report shipped (a41c9f2)
- **Priority:** P1
- **Context:** Found during a run review; the fix needs a decision on what an empty report
  should say, and that decision had not been made. Product wants to sign off the wording before
  any code lands, so this cannot start until that meeting happens.
- **Evidence / code sites:** `pipeline/summarize.py:88`, `pipeline/render.py:24`
- **Blocked by:** —
- **Plan:** `Notes/Plans/2026-03-04-empty-report-handling.md`
- **Closed:** 2026-03-09 — product signed off on "No results for this period." as the
  stated-empty wording; shipped in `a41c9f2`, forced-empty run the same day produced the
  expected output (see `Archive/Phase_02-reporting-hardening/CLOSEOUT.md` §2).

### R7 — Per-account timezone is recomputed per row

- **Status:** open
- **Priority:** P3
- **Context:** Real but not urgent — measured at ~40ms on the largest account, which nobody
  has complained about. Recording it so it is not rediscovered as a surprise.
- **Evidence / code sites:** `pipeline/aggregate.py:112`
- **Blocked by:** —
- **Plan:** —
- **Closed:** —

### R9 — Weekly rollups have the same empty-result gap

- **Status:** blocked — on R4's wording decision
- **Priority:** P2
- **Context:** Same shape as R4, but deliberately out of scope — no reported failure to
  ground the empty-state wording on. Blocked on someone actually hitting it.
- **Evidence / code sites:** `pipeline/rollup_weekly.py:60`
- **Blocked by:** R4 (its wording decision should land first)
- **Plan:** —
- **Closed:** —

### R2 — Mailer retries on 5xx without backoff

- **Status:** done — exponential backoff, capped at 5 (a41c9f2)
- **Priority:** P2
- **Context:** Originally parked behind the ingest rework, which changed the retry surface.
- **Evidence / code sites:** `pipeline/mailer.py:33`
- **Blocked by:** —
- **Plan:** `Notes/Plans/2026-02-18-mailer-backoff.md`
- **Closed:** 2026-02-24 — exponential backoff added, capped at 5 attempts. Verified against a
  forced-5xx run.

### R5 — Cache the account lookup across the whole run

- **Status:** dropped — measured at 8ms, not worth an invalidation problem
- **Priority:** P3
- **Context:** Proposed as an optimisation before anyone measured it.
- **Evidence / code sites:** `pipeline/aggregate.py:44`
- **Blocked by:** —
- **Plan:** —
- **Closed:** 2026-02-20 — dropped. Measured at 8ms total across the largest run; the cache would
  have added an invalidation problem to save nothing. **Kept in the file so it is not re-proposed.**

### R1 — Carried from Phase 1: summary column ordering is non-deterministic

- **Status:** open
- **Priority:** P2
- **Origin:** R1, Phase 1
- **Context:** Cosmetic until a customer diffs two reports. One did, in Phase 1, but the
  phase closed before the fix landed.
- **Evidence / code sites:** `pipeline/render.py:71`
- **Blocked by:** —
- **Plan:** —
- **Closed:** —

---

Notice the gaps: this file shows `R1`, `R2`, `R4`, `R5`, `R7`, `R9` — yet `next_item_id` is
`R12`. `R3`, `R6`, `R8`, `R10` and `R11` existed, closed, and were left behind in an earlier
phase's archive. **IDs are never reused and never renumbered, so the gaps are correct.**
`R2` and `R5` stay here despite being closed and dropped — the record of *why something was
not done* is the most valuable thing in this file.
