# Example — Reference (fictional, for structure only)

Part of one worked example shared across this library: **Meterstream**, an imaginary internal
pipeline that ingests usage events and publishes daily summary reports. Copy the *structure*,
never the content.

Shows the format's two halves: **current understanding on top**, kept correct, and a **dated log
underneath** recording how it was reached — including a later entry that corrects an earlier
claim rather than quietly deleting it.

---

```yaml
---
id: "legacy-summary-job"
schema_version: 1
type: "reference"
title: "The legacy nightly summary job"
summary: "What the pre-pipeline cron job did, which tables it read, and which of its rules the new renderer must preserve."
created_at: "2026-03-03"
updated_at: "2026-03-21"
status: "active"
supersedes: null
superseded_by: null
project: "Meterstream"
initiative: "Phase 2"
source_paths:
  - "legacy/cron/nightly_summary.sh"
  - "legacy/sql/summary_v2.sql"
companion_docs: ["2026-03-06-reporting-pipeline-dataflow"]
tags: ["legacy", "reporting"]
---
```

# The legacy nightly summary job

**What this covers:** `legacy/cron/nightly_summary.sh` and the SQL it invokes. Read before
changing the new renderer — several of its rules are load-bearing and undocumented elsewhere.

## Current understanding

### `nightly_summary.sh`

Runs at 02:15 UTC. Three steps: truncate a staging table, run `summary_v2.sql`, then invoke the
mailer. **No transaction wraps the three** — a mailer failure leaves staging populated, and the
next run's truncate is what cleans it up. This is why a failed night shows as missing data rather
than stale data.

### `summary_v2.sql`

Reads `events` joined to `accounts` on `events.account_id = accounts.id`, filtered to
`events.kind IN ('usage','adjustment')`.

Three rules worth carrying forward:

| Rule | Where | Why it matters |
|---|---|---|
| `adjustment` rows are summed but never counted | `SUM(...) FILTER (WHERE kind='usage')` on the count column | A month with only adjustments reports zero events but non-zero total — deliberate, and it looks like a bug |
| Accounts with `status='closed'` are included if they had events in the window | the `LEFT JOIN` plus `WHERE` ordering | Dropping them would silently change historical totals |
| Window boundaries use the account's timezone | `AT TIME ZONE accounts.tz` | The boundary differs per account; a naive UTC rewrite shifts every total |

### Relevance to current work

The empty-result case this project is now handling exists in the legacy job too — it emits a mail
with an empty table body and no explanation. That is the behaviour being deliberately replaced,
not preserved. The three rules above **are** to be preserved.

## How this understanding was reached

### 2026-03-03

Read `nightly_summary.sh` and `summary_v2.sql` in full for the first time, prompted by the
empty-report work needing to know what the legacy job did on zero rows. Found the three rules and
the missing transaction. **Recorded the timezone rule as UTC** — taken from `TZ=UTC` at the top of
the shell script.

### 2026-03-21

**Corrects the 2026-03-03 entry.** The timezone rule is **per-account, not UTC**. The `TZ=UTC` in
the shell script only sets the cron process timezone; the SQL overrides it per row with
`AT TIME ZONE accounts.tz`, which I had not read closely. The earlier claim was wrong.

This mattered: the renderer had been written against the UTC reading and shifted totals for every
non-UTC account. Found when an account in `Asia/Kolkata` reported a 5.5-hour boundary shift. The
table above now states the correct rule; the wrong belief is recorded here because it explains
that bug and would otherwise look inexplicable in the git history.

---

# Second example — a run index

A different shape in the same folder: one file per experiment track, indexing the keyed runs under
`research_repository/data/`. Written automatically, same as any other reference.

```yaml
---
id: "retrieval-experiments"
schema_version: 1
type: "reference"
title: "Retrieval quality — experiment track"
summary: "Every run on retrieval quality, what it changed, and which won. Current best: 2026-03-06_11-02-00 at 0.81 recall@10."
created_at: "2026-03-04"
updated_at: "2026-03-07"
status: "active"
supersedes: null
superseded_by: null
project: "Meterstream"
initiative: "Phase 5"
source_paths: ["research_repository/data/Phase_05-retrieval/"]
companion_docs: ["retrieval-approach"]
tags: ["retrieval", "experiments"]
---
```

# Retrieval quality — experiment track

**What this covers:** the retrieval quality track in `research_repository/data/Phase_05-retrieval/`.
**Deciding measure:** recall@10 on the 400-question eval set.
**Current best:** `2026-03-06_11-02-00` — 0.81.

## Runs

| Run id | Changed vs previous | Measure | Outcome |
|---|---|---|---|
| `2026-03-04_09-12-00` | baseline, chunk 512 | 0.71 | baseline |
| `2026-03-04_14-30-00` | chunk 512 → 256 | 0.74 | won |
| `2026-03-06_11-02-00` | + reranker | 0.81 | **won — current best** |
| `2026-03-07_16-45-00` | reranker, chunk back to 512 | 0.79 | lost |

**The losing row is the point.** Without it, someone re-tests chunk-512-with-reranker next month
and spends a day rediscovering 0.79. Never prune these.

## What this settled

### 2026-03-06

Reranking is worth its latency; chunk size matters less than expected once reranking is in place.
The decision and its reasoning are in `Notes/Discussions/retrieval-approach.md` — this file is the
index, that one is the argument.
