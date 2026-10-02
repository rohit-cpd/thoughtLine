# Example — Phase closeout (fictional, for structure only)

Part of one worked example shared across this library: **Meterstream**, an imaginary internal
pipeline that ingests usage events and publishes daily summary reports.

This is a **heavy-mode** closeout — all nine sections filled, including the ones that get skipped.
A light-mode closeout keeps only the four sections numbered `L1`–`L4`, which map onto heavy
sections 4, 5, 6 and 9 respectively, plus the debt line. **The archive index the same transition
wrote is at the end of this file** — step 5c's output, and the one document that lands in the
*new* phase rather than in the archive.

**The Meterstream phase had more documents than this library bundles.** Eight `EXAMPLE_*` files
ship here; the tables below cite a few others (`Plans/2026-02-18-mailer-backoff.md`,
`References/mailer-api.md`, `Notes/2026-02-14-notes.md`) that exist only inside the fiction. That
is deliberate — a closeout whose every citation resolved would be a closeout of a two-document
phase, which is not what one looks like. Do not go looking for those files.

---

```yaml
---
id: "phase-02-closeout"
schema_version: 1
type: "phase_closeout"
title: "Phase 2 — Reporting hardening — closeout"
summary: "Reporting stage made reliable end to end; empty-result handling shipped, weekly rollups deliberately untouched."
date: "2026-03-31"
phase_number: "02"
phase_slug: "reporting-hardening"
initiative: "Phase 2"
aliases: ["Reporting Sprint", "Q1 reporting work"]
boundary_type: "clean_break"
next_initiative: "Phase 3"
mode: "heavy"
closeout: "full"
summarized: true
documents_inventoried: 14
documents_unattributed: 0    # nothing in this phase needed batch attribution; §9 Unclassified
                              # lists items that were never attributed at all, which this field
                              # doesn't count — see phase-transition/SKILL.md for the distinction
---
```

# Phase 2 — Reporting hardening — closeout

## 1. What this phase set out to do

From `PHASE_CONTEXT.md`, written 2026-01-12:

> Make the daily summary path reliable enough that a failure is a real incident rather than a
> weekly occurrence. Success is four consecutive weeks with no failed report.

## 2. What was delivered

- **Empty-result handling** — stated-empty report at the render boundary.
  *Evidence:* `main@a41c9f2`; forced-empty run 2026-03-09 produced the expected output.
- **Mailer backoff** — exponential, capped at 5 attempts. Backlog `R2`.
  *Evidence:* forced-5xx run 2026-02-24.
- **Four clean weeks** — 2026-03-02 through 2026-03-29, zero failed reports.
  *Evidence:* run log; this is the phase's stated success criterion, met.

## 3. What was not delivered

- **Column-ordering determinism** (`R1`) — carried since Phase 1, still open.
- **Per-account timezone recomputed per row** (`R7`) — raised during the timezone decision above,
  never scheduled. No correctness impact found; it is a cost item, which is why it slipped.
- **Empty-result handling for weekly rollups** (`R9`) — deliberately out of scope, see §7.
- **Ingest validation rewrite** — *believed* done mid-phase, but never verified against malformed
  input. Recorded here rather than in §2 for exactly that reason.

This section is **selective narrative**, not the mechanical list — §5 is the complete carry
table, and the two are allowed to differ in emphasis. They should not differ in *membership*
though: every ID named here appears there.

## 4. Decisions still binding

| Decision | Why | Source |
|---|---|---|
| A zero-row aggregate is a valid result; empty is handled at the render boundary | Guarding in `aggregate()` pushes the decision onto every future caller | `Discussions/empty-report-handling.md` |
| Report window boundaries use the account's timezone, not UTC | A UTC rewrite silently shifts every historical total | `References/legacy-summary-job.md` |
| `adjustment` rows are summed but never counted | Inherited from the legacy job; changing it alters published history | same |

## 5. Carried forward

| ID | From | Title |
|---|---|---|
| `R1` | `reporting-backlog.md` | Summary column ordering is non-deterministic |
| `R7` | `reporting-backlog.md` | Per-account timezone recomputed per row |
| `R9` | `reporting-backlog.md` | Weekly rollups have the same empty-result gap |

## 6. Open questions still unanswered

Copied verbatim from `PHASE_CONTEXT.md` at the boundary — decisions this phase needed and did
not make. `phase-context` puts these into the next phase's `INHERITED.md`.

1. **`R1` — fix or drop?** Column-ordering determinism has been carried since Phase 1 with no
   reported failure. Phase 3 either schedules it or drops it; carrying it a third time unread is
   the outcome to avoid.
2. **Retry telemetry** — should mailer-backoff attempts be logged per-attempt or only on final
   failure? Raised during the backoff work, never settled.

## 7. Deliberately abandoned

- **Account-lookup caching** (`R5`) — measured at 8ms across the largest run. The cache would have
  added an invalidation problem to save nothing. **Do not re-propose without a measurement.**
- **Fixing weekly rollups alongside R4** — no reported failure to ground the empty-state wording
  on. Guessing at a second message with no real case was judged worse than leaving it.

## 8. Unresolved contradictions

`Architecture/2026-03-06-reporting-pipeline-dataflow.md` shows `ingest.py` writing directly to
`staging`, while `References/legacy-summary-job.md` describes a truncate step
that no current component owns. Both may be right — the truncate may have moved to the scheduler —
but nobody confirmed it. **Recorded as unresolved; not silently reconciled.**

## 9. Unclassified

- `Notes/scratch/` — three untitled files, moved as found.
- `Notes/2026-02-14-notes.md` — no frontmatter, no `initiative`. Could not be attributed; the user
  confirmed it belongs to Phase 2 but it is listed **here** rather than counted in
  `documents_unattributed`. That field counts documents batch-attributed under Step 1's
  "most/all lack frontmatter" rule; this one was attributed individually, by asking. The two look
  alike and are not — which is why the field is `0` above even though this section is not empty.


---

# The archive index the same transition wrote

Step 5c writes this into the **new** phase's `Notes/References/phase-02-archive-index.md`, not
into the archive. It carries the **next** phase's `initiative`, because it is a Phase 3 document
describing Phase 2 — the same Phase 3 whose `PHASE_CONTEXT.md` and `INHERITED.md` are in
`phase-context/EXAMPLE_PHASE_CONTEXT.md`.

```markdown
---
id: "phase-02-archive-index"
schema_version: 1
type: "reference"
title: "Phase 02 — archive index"
summary: "What Phase 2 produced and decided, and where each document now sits."
date: "2026-03-31"
status: "active"
superseded_by: null
initiative: "Phase 3"
source_paths: ["Archive/Phase_02-reporting-hardening/"]
companion_docs: ["phase-02-closeout"]
---

# Phase 02 — what was produced and decided

Everything referenced below lives in `../../Archive/Phase_02-reporting-hardening/`.

## References written
| Document | What it covers | Still relevant |
|---|---|---|
| `References/legacy-summary-job.md` | The pre-pipeline nightly job: tables, joins, and its three timezone/counting rules | **Yes** — those rules still bind |
| `References/mailer-api.md` | The vendor mail API as of v2 | Superseded by the v3 migration |

## Discussions held, and what each decided
| Document | Decided |
|---|---|
| `Discussions/empty-report-handling.md` | An empty result set renders a stated-empty report; the check lives at the render boundary, not in `aggregate()` |
| `Discussions/2026-02-09_Retry_Policy.md` | Exponential backoff capped at 5 attempts; no retry on 4xx |

## Plans written
| Document | Planned | Landed |
|---|---|---|
| `Plans/2026-03-04-empty-report-handling.md` | Render-boundary empty check | Yes — `main@a41c9f2` |
| `Plans/2026-02-18-mailer-backoff.md` | Retry backoff | Yes |

## Key decisions taken this phase
1. Zero-row aggregates are valid; empty is handled at the render boundary.
2. Report windows use the account's timezone, not UTC.
3. Weekly rollups deliberately left alone — no reported failure to ground the wording on.

*Which of these still bind is recorded in `Project_Context/Key_Decisions.md` — that ledger is
authoritative, and a decision superseded later stays listed above because it still happened.*

## Open questions carried into the next phase
From the archived `PHASE_CONTEXT.md`, the `Discussions/` logs' *Still open* entries, and the
phase's plans — decisions the phase needed and did not make. Also in the closeout; repeated here
because the archive index is what a new phase reads first.
1. Reject vs quarantine for malformed rows — never decided.
2. `R1` (column ordering) carried two phases now — fix or drop?

## Architecture
Current architecture is `Project_Context/System_Understanding.md`, **not** a copy here. The
archived diagrams show how it looked during this phase:
- `Architecture/2026-03-06-reporting-pipeline-dataflow.md` — as of `main@a41c9f2`

## Chronology summaries
- `_Summary/References.md`, `_Summary/Discussions.md` — how the thinking moved
  (or: *not written — light transition. Run `phase-transition` on this archive to generate.*)

## Earlier phases
`Archive/Phase_01-ingest-rewrite/`
```

Two things to copy from this, rather than from the template in `SKILL.md`:

- **`Still relevant` is filled in only where it is known.** `legacy-summary-job.md` is marked
  relevant because a binding decision rests on it; `mailer-api.md` is marked superseded because a
  later document replaced it. A document nobody could judge gets a blank cell, not a guess.
- **Every row points into the archive; none of them restates it.** The index is navigation, and a
  second copy of the content here would drift from the immutable original.
