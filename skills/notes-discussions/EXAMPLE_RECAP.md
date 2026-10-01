# Example — Discussion log (fictional, for structure only)

Part of one worked example shared across this library: **Meterstream**, an imaginary internal
pipeline that ingests usage events and publishes daily summary reports. Copy the *structure*,
never the content.

Shows **two rounds on one topic**, which is the point of the format: the file is a log, not a
recap. The second round reverses a decision from the first, and the first is left intact.

The `Notes/Plans/...` link below points into a project's own tree, not into this library — **it
does not resolve here, deliberately.**

---

```yaml
---
id: "empty-report-handling"
schema_version: 1
type: "discussion"
title: "What an empty report should say"
summary: "An empty result set renders a stated-empty report. Weekly rollups were initially out of scope; that was reversed on 2026-03-18."
created_at: "2026-03-02"
updated_at: "2026-03-18"
status: "active"
supersedes: null
superseded_by: null
project: "Meterstream"
initiative: "Phase 2"
participants: ["Dana (product)", "Claude (analysis)"]
decisions_count: 5
backlog_items: ["R4", "R9"]
companion_docs:
  - "2026-03-04-empty-report-handling"
tags: ["reporting", "error-handling"]
---
```

# What an empty report should say

**Topic:** what the daily summary emits when the aggregate returns zero rows, and which report
types that rule covers. Does **not** cover what the aggregate itself should do — zero rows is
valid and that is settled elsewhere.

**Participants:** Dana (product), Claude (analysis)
**Companion docs:** `Notes/Plans/2026-03-04-empty-report-handling.md` · backlog `R4`, `R9`

**Where it currently stands:** decided and shipped for the daily summary; extended to weekly
rollups on 2026-03-18 after one actually failed. No open questions.

---

## 2026-03-02

### What prompted this round

On 2026-02-28 a filter change produced an empty result set and `summarize.py` raised on an empty
aggregate, which surfaced to three customers as a failed report rather than an empty one. No
decision existed for what an empty report should contain, so the crash was being patched ad hoc
in two places.

### The ask, as stated

> Reports are failing when there's no data. Can we just not crash?

Refined in the follow-up round:

> Actually the crash isn't the problem — a blank report would be worse. If there's genuinely no
> usage I want the customer to see that stated, not an empty page they'll read as a bug on our end.

### Decisions

| # | Topic | Decision |
|---|---|---|
| 1 | Empty result behaviour | Render a report stating "no usage recorded in this period" — never fail, never emit a blank page |
| 2 | Where the check lives | At the render boundary, not in the aggregation step — aggregation legitimately returns zero rows |
| 3 | Scope | Daily summary only. Weekly rollups keep current behaviour until someone reports the same issue there |

### Why

Guarding inside `aggregate()` was considered first and rejected: an empty aggregate is a valid
result, and making it an error there would push the same decision onto every future caller. The
render boundary is the only place that knows a human will read the output.

Decision 3 looks arbitrary and is deliberate — nobody has actually seen this fail on weekly
rollups, and fixing it there would mean guessing at a second empty-state message with no reported
case to ground it.

### Next actions agreed

1. Write the implementation plan covering the render-boundary check.
2. Log the work as backlog item `R4` so it stays visible if the plan slips.

---

## 2026-03-18

### What prompted this round

A weekly rollup hit the empty case on 2026-03-16 — exactly what decision 3 was waiting for. One
customer saw the blank page the daily summary no longer produces.

### Decisions

| # | Topic | Decision |
|---|---|---|
| 4 | Weekly rollups | **Reverses decision 3.** Weekly rollups use the same stated-empty path. The reported failure is the grounding that was missing in March |
| 5 | Wording | Same sentence as the daily report, with the period substituted — not a second message to maintain |

### Why

Decision 3 was correct on the information available and is left in the log unchanged: the reason
to wait was that nobody had hit it, and that stopped being true. Decision 5 exists because the
obvious move — a bespoke weekly wording — was what decision 3 was trying to avoid in the first
place.

### Next actions agreed

1. Reopen `R9` and point it at the existing plan rather than writing a new one.
