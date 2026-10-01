# Example — Plan (fictional, for structure only)

Part of one worked example shared across this library: **Meterstream**, an imaginary internal
pipeline that ingests usage events and publishes daily summary reports. Copy the *structure*,
never the content.

The `../Discussions/...` link below points into a project's own `Notes/` tree, not into this
library — **it does not resolve here, deliberately.** It is showing how a real plan cites the
discussion that produced it. Do not go looking for that file.

---

```yaml
---
# --- required ---
id: "2026-03-04-empty-report-handling"
schema_version: 1
type: "plan"
title: "Empty-report handling at the render boundary"
summary: "Add a stated-empty path to the daily summary renderer so a zero-row aggregate produces a readable report instead of a crash."
date: "2026-03-04"
status: "draft"
initiative: "Phase 2"
companion_docs:
  - "empty-report-handling"
supersedes: null
superseded_by: null

# --- optional: only the ones with a real value are here ---
created_at: "2026-03-04T09:15:00+00:00"
updated_at: "2026-03-04T09:15:00+00:00"
generator: "notes-plans / claude-opus-5"
source: { type: "ai_conversation", location: "Empty-report discussion, 2026-03-02" }
project: "Meterstream"
domain: "Reporting"
team: "Data Platform"
owner: "Dana"
tags: ["reporting", "error-handling"]
priority: "P1"
effort_estimate: "S"
---
```

# Empty-report handling at the render boundary

**Goal:** a zero-row aggregate produces a report that states there was no usage, rather than
raising or emitting a blank page.

**Related docs:** decided in
[empty-report-handling](../Discussions/empty-report-handling.md) ·
tracked as backlog item `R4`

## Context and assumptions

- `aggregate()` returning zero rows is valid and stays valid — this is not a bug to fix upstream
  (decision 2 in the companion recap).
- Only the daily summary is in scope. Weekly rollups are explicitly excluded (decision 3).
- The renderer already has a template layer, so the empty case is a template branch rather than
  new infrastructure.

## Steps

1. Add an `is_empty` check at the top of `render_summary()` — before any template selection.
2. Add an `empty.html.j2` template carrying the agreed wording.
3. Emit a structured log line on the empty path so the frequency is measurable; this is currently
   unknown and decides whether step 4 is ever needed.
4. *(Deferred)* If empties turn out to be frequent, revisit whether the report should be sent at
   all. Not decided — see open questions.

## Options considered

| Option | Verdict |
|---|---|
| Guard inside `aggregate()` | Rejected in the discussion — pushes the decision onto every caller |
| Skip sending the report entirely | Rejected for now — silence is indistinguishable from a delivery failure |
| Render a stated-empty report | **Chosen** |

## Open questions

1. How often does this actually fire? Step 3 exists to answer it; nothing else should be decided
   until it has.
2. Weekly rollups have the same shape and no reported failure. Left alone deliberately.
