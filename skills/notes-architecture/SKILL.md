---
name: notes-architecture
description: 'Use when the user wants system/data architecture designed, documented, diagrammed, or explained (e.g. component diagrams, data flow, pipeline architecture, integration architecture) based on the chat discussion — including diagrams of existing systems, and however they phrase the ask. **Only on the user''s request — ask before writing or editing any diagram, including refreshing one that has gone stale.** Saves the architecture writeup as a markdown file with structured frontmatter in Notes/Architecture/ instead of only replying in chat. Not for a forward implementation plan or tradeoffs writeup with no structural view — that is `notes-plans`. Not for explaining existing code, data or config that is not primarily about how components connect — that is `notes-references`.'
---

# Notes Architecture

When producing an architecture description, diagram, or design for a system/data flow/pipeline discussed in chat — including a structural view of an *existing* system — write it to a new file under `Notes/Architecture/` in addition to summarizing it in chat.

## Write scope

Writes only to `Notes/Architecture/`. Never `Project_Intent/`, `Project_Context/`, `Archive/`,
source files, or another `notes-*` folder — each has its own owner. In particular
`Project_Context/System_Understanding.md` is the natural destination for what this skill produces
and is **not** this skill's to write — offer that update in one line instead. Where a diagram
contradicts `Project_Intent/Technical_Specifications.md`, say so and reconcile neither.

**Only on request — for writing *and* for editing.** This is the strictest of the five notes
skills, and deliberately so: unlike a plan or a backlog, an architecture document is a statement
about how the system is built, and changing one without being asked changes the record of what
the system *is*.

- **New diagram** — ask. If the conversation makes one look worth drawing and nobody asked, say
  so in one line and move on.
- **Existing diagram now stale** — **ask; do not refresh it on your own.** Code moving on is not
  permission to redraw. Say which diagram the change affects and that its `ref` is now behind,
  and let the user decide whether to update it, supersede it, or leave it as the record of how
  things looked at that commit. All three are legitimate, and only they can choose.

If `Notes/` isn't scaffolded yet, say so and point at `phase-context`, which owns that. The
project's agent instructions may narrow this scope; nothing widens it.

## When to use
- User wants a system, pipeline, integration, or data flow designed, diagrammed, or its architecture explained — however they word it.
- User asks for a visual/textual representation of how components fit together (e.g. Mermaid diagrams, component breakdowns) — this applies whether the system is new or already exists.
- Not for a forward-looking implementation plan or tradeoffs writeup with no structural diagram — use `notes-plans` for those.
- Not for reference documentation of existing legacy files/code that isn't primarily about how components fit together — use `notes-references` for those.
- Not for a recap of the discussion that led to the design — use `notes-discussions` for that (link it via `companion_docs`).
- Not for tracking open/deferred structural work — use `notes-backlogs`.
- Not for summarizing what a whole phase delivered — use `phase-transition`.

## File naming
`Notes/Architecture/<YYYY-MM-DD>-<short-kebab-case-topic>.md`
(e.g. `Notes/Architecture/2026-08-11-anomaly-detection-pipeline-architecture.md`)

## Frontmatter

The keys under **required** are always present — `phase-transition` at the boundary, the other
`notes-*` skills, and cross-doc linking depend on them. For an architecture doc, `ref` is
required too: a diagram with no record of which commit it reflects is nearly useless a phase
later. Everything under **optional** is exactly that: **fill it when you have a real value,
otherwise leave the key out** — don't write a placeholder or `null` just to keep the shape.

```yaml
---
# --- required ---
id: "2026-08-11-anomaly-detection-pipeline-architecture"   # the filename without .md
schema_version: 1
type: "architecture"
title: "Document title"
summary: "One or two sentences."             # phase-transition builds the archive index from this
date: "2026-08-11"
status: "draft"              # draft | active | locked | completed | superseded | archived
initiative: "Phase 5"        # phase marker — copy verbatim; this is how phase-transition finds the doc
companion_docs: []           # ids of same-topic plan/reference/discussion docs; [] if none
supersedes: null
superseded_by: null
ref: "branch-or-commit-hash" # the state of the code this diagram reflects — required
diagram_type: "component"    # component | dataflow | sequence | integration

# --- optional: include only with a real value, else omit the key ---
created_at / updated_at      # ISO timestamps
review_by: "2026-11-01"      # these go stale as code changes — set a date if you can
repo: "repo-name"
paths: ["path/to/component"]
depends_on: [] / blocks: [] / parent: null
reviewed_by / review_date    # only once a human has ACTUALLY reviewed it — never pre-filled
# Free-form, add only if this project already stamps them on every document:
# project, domain, team, owner, visibility, tags, generator, source, session_id
---
```

## Content
- Title + one-line scope of the system/component being described.
- A Mermaid diagram (or diagrams) illustrating components, data flow, or sequence as appropriate.
- Per-component breakdown: responsibility, inputs/outputs, key dependencies.
- Rationale for key architectural decisions, if discussed.
- Open questions / future considerations, if any.
- A "Related docs" line rendered from `companion_docs`/`depends_on` — don't duplicate the content of those docs here, just point to them.

## Worked example

Read [EXAMPLE_ARCHITECTURE.md](EXAMPLE_ARCHITECTURE.md) when you need to see the Mermaid diagram,
component table and rationale sections filled in together. Fictional content — structure only.

## Notes
- Do not overwrite existing architecture files — create a new dated file per topic.
- Keep chat response short; point to the created file rather than repeating it in full.
- Set `ref` to the actual commit/branch analyzed, not just the repo name — that's what makes `review_by` meaningful later.
