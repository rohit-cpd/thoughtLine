# Example — Phase context and inherited handoff (fictional, for structure only)

Part of one worked example shared across this library: **Meterstream**, an imaginary internal
pipeline that ingests usage events and publishes daily summary reports.

Shows **both** files this skill owns, as they look at the start of Phase 3 — immediately after
Phase 2 was archived.

---

# 1. `Notes/PHASE_CONTEXT.md`

```yaml
---
id: "phase-03-context"
schema_version: 1
type: "phase_context"
title: "Phase 3 — Ingest reliability"
phase_number: "03"
phase_slug: "ingest-reliability"
initiative: "Phase 3"
aliases: []
status: "active"
started_at: "2026-04-01"
last_updated: "2026-04-11"
previous_phase: "Phase 2"
---
```

## Goal

Make ingest trustworthy enough that downstream stages can assume their input is well-formed.
Today `aggregate.py` carries defensive checks that exist only because `ingest.py` cannot be
relied on; the outcome of this phase is that those checks can be deleted.

## Scope

| In scope | Out of scope |
|---|---|
| `ingest.py` validation and rejection path | Anything in `render.py` — Phase 2 closed it |
| Malformed-input test coverage | Weekly rollups (`R9` stays parked) |
| Removing downstream defensive checks once ingest is trusted | Performance work (`R7` carried but not scheduled) |

The out-of-scope column is the one that earns its keep — it is what stops the phase sprawling
back into reporting.

## Current focus

Reproducing the malformed-input cases from the incident log as failing tests, before touching
`ingest.py` itself.

## Success criteria

1. Every malformed-input case in the incident log has a failing test that then passes.
2. At least one defensive check is deleted from `aggregate.py` and the suite stays green.

## Open questions

1. Does ingest reject or quarantine a malformed row? Rejecting loses data; quarantining needs a
   place to put it. Not decided.
2. `R1` (column ordering) has been carried through two phases now. Fix it here or drop it?

---

**Every document written this phase carries `initiative: "Phase 3"`** — copy that string verbatim.

---

# 2. `Notes/INHERITED.md`

> *Derived from `Archive/Phase_02-reporting-hardening/CLOSEOUT.md`. Do not edit by hand —
> regenerate instead.*

## What the previous phase delivered

- Empty-result handling at the render boundary — `Archive/Phase_02-reporting-hardening/CLOSEOUT.md` §2
- Mailer backoff, capped at 5 attempts
- Four consecutive clean weeks, the phase's stated success criterion

## Carried forward

| ID | Title |
|---|---|
| `R1` | Summary column ordering is non-deterministic |
| `R7` | Per-account timezone recomputed per row |
| `R9` | Weekly rollups have the same empty-result gap |

All three are in `Notes/Backlogs/reporting-backlog.md` with their original IDs and origin lines.

## Constraints that still bind

See `Project_Context/Key_Decisions.md` — three decisions from Phase 2 remain binding, covering
empty-result placement, timezone handling, and adjustment-row counting. **Not restated here**;
that ledger is authoritative and a copy would drift.

## Deliberately abandoned

- Account-lookup caching (`R5`) — measured at 8ms; do not re-propose without a measurement.
- Fixing weekly rollups alongside `R4` — no reported failure to ground the wording on.

## Known unresolved contradictions

The Phase 2 architecture doc and the legacy reference disagree about which component owns the
staging truncate. Carried across unresolved.

## Open questions inherited

From the Phase 2 closeout's *Open questions still unanswered*:

1. `R1` (column ordering) — fix or drop? **In scope this phase** (see the scope table above) —
   Phase 3 decides it rather than carrying it a fourth time.
2. Retry telemetry — per-attempt logging or final-failure only? Not in scope; carried on.
