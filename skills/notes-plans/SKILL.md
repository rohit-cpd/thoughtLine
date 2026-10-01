---
name: notes-plans
description: 'Use when the user asks for a plan, design doc, implementation approach, considerations/tradeoffs writeup, or any other intermediary planning artifact — in whatever words they ask for it. Also use **without being asked** when work or a decision has made an existing draft/active plan in Notes/Plans/ out of date — update that plan in place. Creating a new plan file needs the user''s go-ahead; keeping an existing one current does not. Saves plans as markdown files with structured frontmatter in Notes/Plans/. Not for a component or data-flow diagram of how the pieces fit together — that is `notes-architecture`, even while the system is still being designed. Not for a recap of the conversation that produced the plan — that is `notes-discussions`. Not for a running list of open or deferred work — that is `notes-backlogs`.'
---

# Notes Plans

When producing a plan, design proposal, list of considerations, or other intermediary (non-final-code) artifact for the user, write it to a new file under `Notes/Plans/` in addition to summarizing it in chat.

## Write scope

Writes only to `Notes/Plans/`. Never `Project_Intent/`, `Project_Context/`, `Archive/`, source
files, or another `notes-*` folder — each has its own owner.
`Project_Intent/Technical_Specifications.md` is where a plan may *look* like it belongs; it does
not. If the plan changes how the system is understood, say so in one line and let the user
decide — and where it contradicts the spec, report the divergence rather than reconciling it.

**Creating a new plan file needs the user's go-ahead. Keeping an existing one current does not.**
The two halves are governed separately:

| | Permission |
|---|---|
| **New plan file** | **Ask first.** If the user starts something new and no plan covers it, don't write one silently and don't skip it either — say a plan would help, ask whether to create it, and wait. |
| **Existing plan, `status: draft` or `active`** | **Edit it on your own.** No permission needed. |
| **Existing plan, `status: locked`/`completed`/`superseded`** | **Ask.** In-place editing is already closed off (see *Notes*), so what's needed is a new file — which is the row above. |

**Keeping an active plan current is the automatic half, and it is the one people forget.** When
the user changes code, settles something the plan listed as an open question, or picks one of its
considered options, update the plan then and there — they will usually not think to ask. Resolve
the open-questions item, mark the decision, note what actually changed, bump `updated_at`. A plan
that silently stops describing the work is worse than no plan, because it is still read as
current.

If `Notes/` isn't scaffolded yet, say so and point at `phase-context`, which owns that. The
project's agent instructions may narrow this scope; nothing widens it.

## When to use
- User asks for a plan, implementation approach, or tradeoffs writeup for something not yet built.
- Not for a component/data-flow diagram of how a system is or will be structured — use `notes-architecture` for that, even if the system is still being designed. A plan can still *reference* a diagram produced there rather than reproducing it.
- Not for a recap of the conversation that led to this plan (what was asked, what was decided, why) — use `notes-discussions` for that and link it via `companion_docs`.
- Not for documenting existing code/data — use `notes-references`.
- Not for tracking a list of open/deferred work — use `notes-backlogs`, which owns a living
  file updated in place. A plan covers *how to build one thing*; the backlog is the list of
  things not yet built. A backlog item should link to its plan, not contain it.
- Not for summarizing what a whole phase delivered — use `phase-transition`.

## File naming
`Notes/Plans/<YYYY-MM-DD>-<short-kebab-case-topic>.md`
(e.g. `Notes/Plans/2026-08-06-snowflake-migration-plan.md`)

## Frontmatter

The keys under **required** are always present — `phase-transition` at the boundary, the other
`notes-*` skills, and cross-doc linking depend on them. Everything under **optional** is exactly
that: **fill it when you have a real value, otherwise leave the key out.** Don't write a
placeholder or `null` just to keep the shape — an absent key reads as "not recorded", which is
honest. If the project already stamps every doc with `project` / `team` / `owner`, follow that;
otherwise skip them.

```yaml
---
# --- required ---
id: "2026-08-06-snowflake-migration-plan"   # the filename without .md
schema_version: 1
type: "plan"
title: "Document title"
summary: "One or two sentences."             # phase-transition builds the archive index from this
date: "2026-08-06"
status: "draft"              # draft | active | locked | completed | superseded | archived
initiative: "Phase 5"        # phase marker — copy verbatim; this is how phase-transition finds the doc
companion_docs: []           # ids of same-topic architecture/reference/discussion docs; [] if none
supersedes: null             # id of the doc this replaces, or null
superseded_by: null          # set only when a later doc replaces this one

# --- optional: include only with a real value, else omit the key ---
created_at / updated_at      # ISO timestamps
priority: "P2"               # P0 | P1 | P2 | P3
effort_estimate: "M"         # S | M | L, or story points
due_date: "2026-09-01"
depends_on: []               # plan/doc ids this one needs done first
blocks: []                   # ids waiting on this
parent: null                 # parent plan id, when this plan is one step of a sequence
reviewed_by / review_date    # only once a human has ACTUALLY reviewed it — never pre-filled
review_by: null              # a date, only once a review is actually scheduled
# Free-form, add only if this project already stamps them on every document:
# project, domain, team, owner, visibility, tags, generator, source, session_id
---
```

## Content
- Title + one-line goal
- Context/assumptions
- Plan steps or considered options with tradeoffs
- Open questions / decisions needed
- A "Related docs" line rendered from `companion_docs`/`depends_on` — don't duplicate the content of those docs here, just point to them.

## Worked example

Read [EXAMPLE_PLAN.md](EXAMPLE_PLAN.md) when you are unsure how much detail a plan needs, or how
it should cite the discussion that produced it. Fictional content — copy the structure only.

## Notes
- **One dated file per plan — but the same plan evolving is not a new plan.** While `status` is
  `draft` or `active`, edit it in place across as many conversations as it takes, bumping
  `updated_at`. **A feature change is a new plan**, not an edit: start a new dated file once the
  scope has grown past what the original covered, or `status` has reached
  `locked`/`completed`/`superseded`. Creating it needs the user's go-ahead — see *Write scope*.
- **Record the chain with `superseded_by` / `supersedes`, always — not `companion_docs`.** When a
  new plan replaces an older one, set `superseded_by: "<new plan id>"` on the old file and
  `supersedes: "<old plan id>"` on the new one, and set the old file's `status: superseded`.
  `companion_docs` and `depends_on` say *these are related*; only this pair says **which replaced
  which**, which is what you need to walk back from the current plan to the reasoning it came
  from. Stamping the old file is an edit to an existing plan, so it needs no permission — do it
  in the same breath as creating the new one, or the chain has a hole in it.
- Keep chat response short; point to the created file rather than repeating it in full.
- If the plan defers anything, record the deferral via `notes-backlogs` as well; a deferred
  item that lives only inside a plan is invisible to "what's left".
- `reviewed_by`/`review_date` stay `null` until a human actually checks the plan — don't imply review happened.
