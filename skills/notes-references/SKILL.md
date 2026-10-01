---
name: notes-references
description: 'Use whenever existing files/folders/code/data (e.g. legacy scripts, SQL files, data dictionaries, config files, third-party sources) have been researched or explained and the subject is durable enough that re-deriving it later would be real work — record it without being asked. One undated file per topic in Notes/References/, grown over time: **append a dated entry to the existing file** when more is learned about a subject already covered, and start a new file when the subject is new. Ask when unsure whether something is worth recording or which topic it belongs to. Also use when the user explicitly asks for a writeup. Not for a throwaway question about a line or two — answer in chat only. Not for comments inside the code itself — that is `document-code-comments`.'
---

# Notes References

When producing a detailed explanation, research summary, or documentation of existing
files/folders/code/data for the user's future reference (as opposed to a forward-looking plan —
see the `notes-plans` skill for that), write it to a new file under
`Notes/References/` in addition to summarizing it in chat.

## Write scope

Writes only to `Notes/References/`. Never `Project_Intent/`, `Project_Context/`, `Archive/`,
source files, or another `notes-*` folder — each has its own owner. A reference records how
something actually works, which is `Project_Context/` territory: offer the
`System_Understanding.md` update in one line instead of making it, and where a reference
contradicts `Project_Intent/Technical_Specifications.md`, report the divergence rather than
reconciling it.

**No permission needed, for a new file or an append.** When the durability test below is met,
write it — don't ask first and don't offer instead.

| | Permission |
|---|---|
| **New topic file** | **Automatic.** If the subject is durable and nothing covers it, write it. |
| **Existing topic file** | **Append on your own** — see *Appending to a topic file*. |
| **Genuinely unsure** | **Ask.** Whether it is worth recording at all, or which topic file it belongs to — either way, one line and wait. |

The thing to avoid is not writing too much; it is writing something **confidently wrong**, or
scattering one subject across three files. Where either is a live risk, ask.

If `Notes/` isn't scaffolded yet, say so and point at `phase-context`, which owns that — don't
create the tree here. The project's agent instructions may narrow this scope; nothing widens it.

## When to use
- User wants a folder / file / dataset / legacy codebase written up as a document they can come
  back to — however they word it.
- User asks for a detailed reference on how something works (e.g. a report, script, schema) so it
  doesn't need to be re-derived later.
- **The test is whether the subject is durable, not which verb was used.** This skill fires on the
  research having been done, not on a request for it. If you have just read a legacy script, a
  schema, a config file or a multi-file subsystem closely enough that re-deriving it later would be
  real work, record it — nobody has to ask. "Make sense of this script" produces both a chat answer
  and a file.
- **A throwaway question still gets a chat answer only.** "What does this line do", "which of these
  two flags is set" — the subject isn't durable, so there is nothing worth keeping. Where it is
  genuinely borderline, write it: a wrong entry is corrected by a later dated one that says what
  it corrects, so the cost of writing too soon is low.
- Not for forward-looking plans, designs, or proposals — use `notes-plans` for those instead.
- **Not comments inside the source** — that is `document-code-comments`. **"Explain this module"
  matches three outputs**: a file here, edited source, or a chat answer with no artifact. Decide by
  which output is wanted and **ask when unclear** — writing automatically makes a wrong guess more
  expensive, since no permission prompt stands in the way.
- **Not deferred or open work** — that is `notes-backlogs`. A reference describes what exists; if
  the document will need editing every time an item is finished, it belongs in the backlog folder.
- Not a project-wide "where do we stand" answer — use `project-state-brief`.
- **A known limitation counts as a reference** — a partly-mitigated, standing concern is still a
  fact about how the system behaves today. But if it is actively still being decided, the decision
  belongs in `notes-discussions` and the follow-up in `notes-backlogs`.

## File naming — deliberately undated

`Notes/References/<topic-slug>.md`
(e.g. `Notes/References/legacy-billing-scripts.md`, `Notes/References/events-schema.md`)

**Never put a date in the filename.** One file per subject, grown as more is learned — a date
would be wrong the first time you appended. `updated_at` records recency; the dated sections in
the body record what was learned when.

**One file per subject, and "same subject" is a judgement call.** Before starting a new file, list
what is already in `Notes/References/` and append to an existing one if it clearly covers the same
subject. **When it is borderline, ask.**

**Two files here are written by other skills. Neither is a topic file; leave both alone.**

| File | Owner |
|---|---|
| `phase-<NN>-archive-index.md` | `phase-transition`, at each boundary |
| `project-state-brief.md` | `project-state-brief`, when the user asks for a brief on disk |

Do not append to either, and do not treat their subjects as covered — a real reference about the
same material is still yours to write.

## Frontmatter

Deliberately leaner than `notes-plans` — a reference has no priority, effort, or due date.
Every key below is **required and always present** (`[]` when a list is genuinely empty), except
`project` and `tags` which are **optional — omit the key if there is no real value.**

```yaml
---
id: "legacy-billing-scripts"   # the filename without .md — the subject slug
schema_version: 1
type: "reference"
title: "Document title"
summary: "One or two sentences."   # phase-transition builds the archive index from this
created_at: "2026-08-10"     # first entry
updated_at: "2026-09-02"     # last entry — bump on every append; the only freshness signal
status: "active"             # active | superseded | archived
supersedes: null             # the archived predecessor, when a subject continues across a phase
                             # boundary — a PATH, not an id, since topic ids repeat per phase
superseded_by: null          # only when a whole subject is replaced by a differently-scoped one;
                             # appending within a subject supersedes nothing
initiative: "Phase 5"        # phase marker — copy verbatim; this is how phase-transition finds the doc
source_paths: []             # what was actually read to produce this; [] if none
companion_docs: []           # ids of same-topic docs; [] if none
project: "Project Name"      # optional
tags: []                     # optional
---
```

## Content — current understanding on top, dated log underneath

A reference is read to answer "how does this work", so the readable description stays at the top
and is kept current. The chain of how that understanding was reached lives below it.

**What this covers** — one-line scope and the `source_paths` actually read.

**Current understanding** — the body of the document, rewritten as it improves:

- Per-file or per-component breakdown: purpose, key fields/tables/APIs, notable business logic.
- Concrete details — table names, key columns, join conditions, code snippets. **Favour detail
  and precision over brevity**, since the whole point is not having to re-derive the source.
- A closing part connecting findings to work in progress — which tables, columns or rules matter
  to what is being built now.
- Mark anything you could not verify as unverified, rather than asserting it.

**How this understanding was reached** — `### <YYYY-MM-DD>` entries, oldest first, newest
appended. One per research round: what was read, what was learned, and **what it corrected**.

## The run index — one topic file per experiment track

A research phase accumulates many keyed runs, each with its own `RUN.md`. Nothing else in this
library lists them, so "what have we already tried, and what won?" otherwise means opening every
run folder and reconstructing the comparison by hand — and the runs that **lost** get forgotten
first, which is how the same approach gets tested twice.

**One undated file per experiment track:** `Notes/References/<track-slug>-experiments.md`
(e.g. `retrieval-experiments.md`). Write it automatically, like any other reference. It holds a
*What this covers* / *Deciding measure* / *Current best* header, a **Runs** table, and a dated
*What this settled* log — [EXAMPLE_REFERENCE.md](EXAMPLE_REFERENCE.md) shows one filled in.

Rules that make it worth having:

- **One row per run, appended when that run's `RUN.md` Result lands.** Append-only: a row is
  edited once, to fill its `Outcome` when the result arrives, and never again.
- **Link, never copy.** The row is an index entry; `RUN.md` holds the detail and
  `config_used.*` holds the config. Restating either creates a second version that drifts.
- **Keep the losing rows.** They are the most valuable thing in the file — they are what stops
  the same approach being re-tested in three weeks. Never prune them.
- **`source_paths`** points at the track's data folder, so the index says where its evidence is.

`research-to-production-port` reads this file first when deciding which run to port.

## Appending to a topic file

**The description on top is rewritten. The dated log is append-only.**

- **A new round adds a dated entry** and updates *Current understanding* to match.
- **Editing today's entry is fine** while the round is still going.
- **A later finding that contradicts an earlier one must say so.** Correct the description on top,
  and in the dated entry write what the document used to claim and why that was wrong —
  *"2026-09-02: the timezone rule is per-account, not UTC. The 2026-08-10 entry said UTC, read
  from the config default rather than the query."* Deleting the old claim silently is the failure
  mode here: a reference that quietly rewrote itself gives no one a reason to distrust it, and
  the wrong belief usually explains a bug somewhere else.
- **Bump `updated_at`** on every append.

## Worked example

Read [EXAMPLE_REFERENCE.md](EXAMPLE_REFERENCE.md) when you are unsure how much concrete detail a
reference needs — it is the level that makes re-deriving the source unnecessary. Fictional
content — structure only.

## Notes
- One reference file is written by another skill: `phase-transition` puts a
  `phase-<NN>-archive-index.md` here at each boundary. It is a map of the previous
  phase's documents, not a copy of them — leave it alone and do not duplicate its content.
- Do not overwrite existing reference files — create a new dated file per topic. If a later
  document replaces this one, set `status: superseded` and `superseded_by` here rather than
  editing the body.
- Keep chat response short; point to the created file rather than repeating it in full.
