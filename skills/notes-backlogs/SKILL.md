---
name: notes-backlogs
description: >-
  Use when the user asks to track, add, defer, close or re-prioritise a work item,
  or asks what is still open — however they phrase it (e.g. "add this to the
  backlog", "track that for later", "mark it done", "what's left"). Also use
  **without being asked** to keep an existing backlog file in Notes/Backlogs/
  current when code changes or a decision opens, closes or re-prioritises work it
  covers. Creating a new area backlog file needs the user's go-ahead; updating one
  that already exists does not. Maintains a living per-area backlog file
  of open work items with stable IDs, updated in place so it is always current.
  Not for documenting existing code/data (use `notes-references`), not for how to
  build one specific thing (use `notes-plans`), and not for closing out a whole
  phase (use `phase-transition`).
---

# Notes Backlogs

A backlog is the only **mutable** document type in this Notes system. Every other
`notes-*` skill appends a dated, immutable snapshot. This one maintains current state:
one file per work area, updated in place, always reflecting what is open *right now*.

## Write scope

Writes only to `Notes/Backlogs/`. Never `Project_Intent/`, `Project_Context/`, `Archive/`, source
files, or another `notes-*` folder — each has its own owner.

**Creating a new area file needs the user's go-ahead. Keeping an existing one current does not.**

| | Permission |
|---|---|
| **New area backlog file** | **Ask first.** A whole new tracked area is the user's call. If work is being parked and no area file covers it, say so and ask whether to start one — don't write it silently, and don't drop it either. |
| **Existing area file** | **Update it on your own.** Adding an item, closing one, re-prioritising, filling `Closed:` — no permission needed. |
| **The `<area>-closed-backlog.md` companion** | **Ask.** It is a new file, so it falls under the first row (see *When closed items start to dominate a file*). |

**Keeping an existing file current is the automatic half.** When code ships that closes an item,
close it — set the keyword, write the `Closed:` line, leave `Context` intact. When a change or a
decision opens new work in an area already tracked, add the item. When something already tracked
becomes more or less urgent, change its `Priority`. The user will usually not think to ask, and a
backlog that silently stops matching reality is worse than none, because "what's left" is read as
authoritative.

What this does **not** license: inventing a tracked area nobody asked for, and treating another
skill's output as permission. A discussion recap naming untracked work is not authorisation to
start a new area file — offer, and wait.

If `Notes/` isn't scaffolded yet, say so and point at `phase-context`, which owns that. The
project's agent instructions may narrow this scope; nothing widens it.

One exception to all of the above, and it is not a user request: `phase-transition` writes these
files directly at a phase boundary, in this skill's format. See *Across a phase boundary* below.

## When to use
- User defers something, parks an idea, or says "later", "next phase", "not now, but track it".
- User asks what is still open, what is left, or the status of a tracked item.
- User marks an item done, blocked, dropped, or re-prioritized.
- Not for a forward plan of *how* to implement one item — that's `notes-plans`; a backlog
  item should *link* to its plan rather than contain it.
- Not for rolling a phase's open items into the next phase — `phase-transition` writes the new
  phase's backlog files itself, in this skill's format. See *Across a phase boundary* below.

## File naming — deliberately undated

`Notes/Backlogs/<area-slug>-backlog.md`
(e.g. `Notes/Backlogs/ingest-backlog.md`, `Notes/Backlogs/reporting-backlog.md`)

**Never put a date in a backlog filename.** The file is current state, not a snapshot; a date
would go stale the first time an item is closed. The `updated_at` field in frontmatter records
recency instead.

One file per meaningful work area (a stage, a subsystem, a phase). Create a new area file when
items clearly belong to a different unit of work; do not split one area across several files.

## Frontmatter

Every key below is **required and always present**, except `project` and `companion_docs` which
are **optional — omit the key if there is no real value.** `next_item_id` is load-bearing:
`phase-transition` mints continuation IDs from it at a boundary, so it must always be correct.

```yaml
---
id: "reporting-backlog"      # matches the filename without .md
schema_version: 1
type: "backlog"
title: "Reporting — deferred work"
summary: "Open and deferred items for the reporting stage."
created_at: "2026-08-25T10:00:00+05:30"
updated_at: "2026-08-25T10:00:00+05:30"   # bump on every edit
status: "active"             # active | closed (area finished)
initiative: "Phase 2"        # phase marker — must match other docs in this phase verbatim
next_item_id: "R12"          # the next ID to hand out; prevents reuse
project: "Project Name"      # optional
companion_docs: []           # optional; e.g. the closeout id after a carry-forward
---
```

## Item rules (these are what make the file trustworthy)

1. **Stable IDs, never reused.** Prefix by area, number sequentially
   (`R1`, `R2` for reporting; `I1` for ingest).
   Take the next ID from `next_item_id` and bump it. A dropped item's ID is retired, not recycled.
2. **Never delete an item.** Completed, dropped, and superseded items stay with a changed
   `status` — the record of *why something was not done* is often the most valuable thing here.
3. **Never renumber.** Priority is a field, not a position in the list.
4. **One item = one decidable unit of work.** If closing it requires two unrelated decisions,
   split it into two items and cross-link them.
5. **`Status:` is `<keyword> — <short note>`.** The text **before the first ` — `** (or the
   whole value, if there is no ` — `) is **exactly one keyword** — `open`, `in-progress`,
   `done`, `blocked`, `dropped` or `superseded`. After the ` — `, an optional short glance-level
   note (`blocked — waiting on R4`, `done — shipped in a41c9f2`). Tooling and `phase-transition`
   read **only the keyword**; the note is for humans scanning the file. The *detailed* reasoning
   goes in `Context`, never here. **Never put prose where the keyword goes** ("known bug,
   unfixed") — split it: keyword before the dash, prose after it or in `Context`.
6. **Every item lives under a `### <ID> — <title>` heading.** No loose paragraphs, no "misc" or
   "housekeeping" prose outside an item. If a task is worth keeping it is worth an ID.
   Un-itemised text is invisible to `phase-transition`'s carry loop and is lost at the next boundary.

## Item format

```markdown
### R4 — Empty result set crashes the summary step

- **Status:** blocked — needs the empty-report wording decided first
- **Priority:** P1
- **Context:** Found during a run review; the fix needs a decision on what an empty report should
  say, and that decision had not been made. Product wants to sign off the wording first.
- **Evidence / code sites:** `pipeline/summarize.py:88`, `pipeline/render.py:24`
- **Blocked by:** the empty-report wording decision
- **Plan:** `Notes/Plans/2026-03-04-empty-report-handling.md`   <!-- link, never inline -->
- **Progress:**               <!-- optional; append-only, see the table below -->
  - `2026-03-11`: tried X, ruled out because Y
- **Closed:** —
```

`Status:` note, `Context`, `Closed:` do three different jobs:

| Field | Holds | Lifetime |
|---|---|---|
| `Status:` note | a glance-level phrase — what you read scanning the file | changes with the status |
| `Context` | the item's standing explanation — why it is where it is, and the history that matters | **stays with the item after it closes** — so "not urgent at current scale" is never stranded when the status flips to `done` |
| `Progress` (optional) | a dated, append-only log of partial work across sessions — not a restatement of `Context`, which stays the item's standing *why* | grows while the item is open; stops once `Closed:` is written |
| `Closed:` | the closing outcome — date + one line on what actually happened | written once, at close |

Only add `Progress` once an item has actually seen work in more than one session — an empty
`Progress:` field on a brand-new item is noise, not a record.

**Write `Context` for someone who wasn't in the room.** A backlog item is read cold, by a
stranger, more often than anything else in this system. "Deferred because it needed a decision we
hadn't made" is useful; "deferred" alone is not. Avoid session shorthand and bare internal
identifiers. For a defect, name the input that triggers it and the wrong output it produces — not
an abstract description of what's wrong.

## Updating
- Bump `updated_at` on every edit. This is the only signal of freshness the file has.
- When an item closes, set the `Status:` keyword and its short note, fill `Closed:` with the date
  and a one-line outcome, and **leave `Context` intact** — it is now the record of why the item
  took the path it did.
- If a plan or reference doc gets written for an item, add the link to that item — the backlog
  is the index into the rest of `Notes/`.
- Do not summarise the backlog into chat in full; report only what changed.

### When closed items start to dominate a file

Once an area file's `done`/`dropped`/`superseded` items outnumber its `open`/`in-progress`/
`blocked` ones, split the closed items out — don't wait for a phase boundary to do it.

- Move every closed item **verbatim** — `Context`, `Closed:`, everything — into a companion
  file: `Notes/Backlogs/<area-slug>-closed-backlog.md`. The name ends in `-backlog.md` so the
  file matches the folder's convention and is found by tooling that globs for it. This is a move, not a deletion; rule 2
  still applies, it just applies across two files now instead of one.
- Give the companion file the same frontmatter shape, with `status: "closed"` (this file holds
  no open work by definition) and `companion_docs` pointing back at the active file — and the
  active file's `companion_docs` pointing at it in return.
- The active file keeps `next_item_id` — IDs are never split across two counters.
- **Raise it the moment the threshold is crossed**, in one line — the split creates a file, so it
  needs the user's go-ahead (see *Write scope*). Don't sit on it until a boundary: a file that's
  already mostly closed-item noise by the time anyone notices is the failure this exists to
  prevent, and the only way that happens is nobody mentioning it.

## Worked example

The item format above is the spec. Read [EXAMPLE_BACKLOG.md](EXAMPLE_BACKLOG.md) when you need
to see a **whole file with history in it** — items open, done, dropped and carried across a
boundary at once, and why the ID sequence has gaps. Fictional content — structure only.

## Across a phase boundary

`phase-transition` step 5b creates the next phase's backlog files directly. What it does, and
what you must not undo afterwards:

- **IDs never restart.** The new file's `next_item_id` continues the archived file's sequence.
  A reused ID makes two different items look like one across the boundary.
- **`initiative` is the NEW phase's string.** The archived file keeps the old one. This is the
  single field that differs between the two copies.
- **Only items travel whose `Status:` keyword is `open`, `in-progress` or `blocked`** (plus any
  legacy item whose keyword is not one of the six — normalised to `open — <the old prose>`).
  Items whose keyword is `done`, `dropped` or `superseded` stay in the archived file — the
  carried file starts as a clean slate of live work. That history is why the archive exists.
- **Each carried item gains an origin line** — `- **Origin:** R4, Phase 2` — so its lineage
  survives even though its ID did not change.

## Notes
- If asked "what's left" and no backlog file exists yet for that area, offer to create one from
  the open items you can find rather than answering from memory.
- Verify code-site claims before recording them as evidence; an unverified line reference in a
  backlog gets trusted later exactly like a verified one.
