---
name: project-knowledge
description: >-
  Writes and updates the documents that outlive every phase: Project_Intent/ (what
  the project is meant to be — user-owned, edited only on request) and
  Project_Context/ (what we have learned and what is currently true —
  skill-maintained). Name it to update project state, record a decision, refresh the
  system understanding, add a glossary term, or append the timeline. This is the
  write side: not for reading back where things stand or catching up on a project
  ("what's the current state", "where are we") — that is `project-state-brief`,
  which writes nothing. Not for the current phase's scope — that is `phase-context`.
disable-model-invocation: true
---

# Project Knowledge

Owns the documents that outlive every phase. `Notes/` is emptied at each boundary; these are the
continuity across boundaries.

## Write scope

**This skill runs only when the user names it.** It is never a second step of other work, and a
general instruction to write something down does not reach it — "document this" covers `Notes/`,
which other skills own. If work reveals something these files should record and nobody asked, say
so in one line and wait.

Writes `Project_Context/` freely once invoked. Writes `Project_Intent/` **only when the user asks
for that specific change**. Never writes `Notes/`, `Archive/` or source files. The project's agent
instructions may narrow this scope; nothing widens it.

## The distinction — never collapse these

Two folders, two completely different edit rules; keeping them apart is the single most important
thing this skill does.

| | `Project_Intent/` | `Project_Context/` |
|---|---|---|
| Answers | What the project is *supposed* to be | What we have *learned* and what is currently true |
| Owned by | The user | The skills |
| Edited | **Only when the user explicitly asks** | Freely, as understanding changes |
| Stability | High — changes are deliberate pivots | Living — changes constantly |
| If absent | **Leave it absent.** Never create a placeholder | Create when there is real content for it |

**Never write intent from context.** When work reveals something new, it goes in
`Project_Context/` — always. It reaches `Project_Intent/` only when the user says so, in words
like *"update the technical specifications to reflect this."*

A discussion discovers the architecture has changed: update
`Project_Context/System_Understanding.md` and `Key_Decisions.md`; do not touch
`Project_Intent/Technical_Specifications.md`. Same for a limitation surfaced by implementation —
that is context, not intent. Overwriting intent with what happened destroys the only evidence
that the two ever diverged.

**When they do diverge, say so.** If `System_Understanding.md` now contradicts
`Technical_Specifications.md`, report the contradiction to the user and let them decide whether
reality or the spec should change. Do not quietly reconcile it in either direction.

---

## `Project_Intent/` — user-owned

| File | Purpose |
|---|---|
| `Project_Overview.md` | What the project is: the idea, the problem, vision, objectives, scope. **The top-level entry point** — the first thing anyone reads |
| `Business_Model.md` | Business value, users, stakeholders, value proposition, economics |
| `Technical_Specifications.md` | High-level technical requirements, constraints, principles, capabilities |

Rules:

- **Never create a file that does not exist.** A missing `Business_Model.md` means the user has not
  written one; an AI-authored placeholder here is worse than nothing, because it looks like intent
  and is not.
- High level. If a line would change monthly, it belongs in `Project_Context/`.
- On a genuine pivot the user did ask for, keep the previous claim visible so the change is legible
  rather than silent.

## `Project_Context/` — skill-maintained

| File | Purpose | Cadence |
|---|---|---|
| `Project_State.md` | Current state, current phase, current priorities | Every transition + major milestone |
| `System_Understanding.md` | Current understanding of how the system works | Every transition |
| `Key_Decisions.md` | Important decisions and their rationale | Append whenever a decision locks |
| `Project_Timeline.md` | Major events, phases, breakthroughs | Append at every transition + breakthrough |
| `Glossary.md` | Canonical terminology and definitions | Continuously, as terms appear |

Five files rather than one because they change at five different rates. A single document would
need a full rewrite whenever any one of them moved.

## Modes

### `initialize` — first run

Runs before the first phase exists — there is no `Notes/PHASE_CONTEXT.md` yet.

1. Create `Project_Context/` and populate the files you have real content for.
2. Seed from what exists, in order of preference: any existing project-wide summary document
   (whatever this project called it — `PROJECT_SUMMARY.md`, `OVERVIEW.md`, a `README` section),
   then `Archive/*/CLOSEOUT.md`, then the notes trail. **If the only thing that exists is
   `Project_Intent/Project_Overview.md`, seed from it — this is the one sanctioned case of
   deriving `Project_Context/` from intent.** It happens only here, only at first run, and every
   claim taken this way is marked unverified like any other seed.
3. **Mark every seeded claim unverified.** A summary inherited from an older document is a claim
   about the project, not a fact about it — and the first run is exactly when a stale assertion
   gets laundered into a new authoritative file.
4. **Create `Project_Intent/` files only if the user asks.** Offer to draft `Project_Overview.md`
   from what you found; do not write it, or the other two, unprompted.
5. Stamp `last_updated_at_phase: "Seeding Phase"` on every file written here — there is no real
   phase to name yet. `project-state-brief` treats this sentinel as "not yet in a phase", never
   as stale. It stays until the first `update` run (below) replaces it with the real phase.
6. Report what you seeded from, what you left empty, and why.

### `update` — normal operation

Runs whenever the user asks — after `phase-transition` at a boundary, at a milestone, or any time
they want `Project_Context/` back in line with where the project actually is. There is no wrong
moment; the point of this mode is that the files reflect the latest knowledge on demand.

Touch only the files the change affects. Bump `last_updated` and `last_updated_at_phase` on each.
Never rewrite wholesale when appending is correct — `Key_Decisions.md` and `Project_Timeline.md`
are append-only.

**Don't pin an assertion to a sibling-owned file that's about to change in this same sitting.**
Recording "`Notes/PHASE_CONTEXT.md` is stale about X" — a file `phase-context` owns — is wrong the
moment that skill runs later in the session to fix exactly that, and nothing prompts a second pass
to reconcile it. Where the sibling file may still be corrected in this sitting, say it
provisionally ("as of this writing, X; `phase-context` has not yet run to update it") or ask
whether that skill should run first.

**Where the phase name comes from — and why it is not always `PHASE_CONTEXT.md`.** Take it from
`Notes/PHASE_CONTEXT.md`'s `initiative`. But at a phase boundary that file **does not exist
yet**: this skill runs after `phase-transition` (which resets `Notes/` and hands `PHASE_CONTEXT.md`
off without writing it) and before `phase-context` (which writes it). That is the exact window
this mode is designed for, so the absence is normal, not an error. In it, take the phase from the
newest `Archive/*/CLOSEOUT.md`'s `next_initiative` — the string `phase-context` is about to use.
If neither source exists, ask; do not invent a phase name, because every document written under a
wrong one is invisible at the next boundary.

## Shared frontmatter

```yaml
---
id: "project-state"
schema_version: 1
type: "project_context"      # project_context | project_intent
title: "Project State"
last_updated: "2026-09-01"
last_updated_at_phase: "Phase 6"   # staleness signal — see below; "Seeding Phase" at initialize
verified: true                      # false when content is inherited but unchecked
---
```

`last_updated_at_phase` is the staleness mechanism. When it falls behind the current phase in
`Notes/PHASE_CONTEXT.md`, the file is stale by definition and `project-state-brief` flags it — the
cheap check that catches a summary drifting out of date *before* someone acts on it. The
`"Seeding Phase"` sentinel is the exception: seeded, not yet phase-updated, and not stale.

`Project_Intent/` files carry it too, but falling behind there is **expected, not a defect** — a
stable intent document should not be changing every phase. Do not "fix" it by editing the file.

## Per-file notes

**`Project_Overview.md`** — the entry point. A cold reader takes it, then `Project_State.md`, then
`System_Understanding.md`; write it so that order works — what we are building, before where we are.

**`Project_State.md`** — what exists and works, what is scaffolded but unwired, what is planned,
which phase is active. **Never in-flight task detail** — that is `PHASE_CONTEXT.md` and the
backlog. If a line here would change weekly, it belongs there.

**`System_Understanding.md`** — one consolidated description of how the system works *right now*:
components, data flow, where authority for each kind of data lives, what the boundaries are.
Refreshed at each transition from that phase's architecture documents. Detailed and historical
diagrams stay in `Notes/Architecture/` and the archives. State plainly at the top which phase this
reflects — architecture descriptions go stale faster than anything else in a project.

**`Key_Decisions.md`** — the cumulative, append-only ledger of decisions that still constrain the
project, including ones made several phases ago. **Authoritative for decisions.**
`Notes/INHERITED.md` links here rather than restating; phase closeouts are the evidence behind
entries. One row per decision: id, date, phase, decision, one-line why, source link, and status
(`binding` | `superseded by <id>` | `lifted`). Never edit or remove a decision — supersede it with
a new row that points back.

**`Project_Timeline.md`** — append-only narrative spine: phase starts and ends, boundary types,
breakthroughs, significant failures and what they taught. One dated entry per event, newest last.

**`Glossary.md`** — two vocabularies, separate sections, both required:

- **Domain terms** — the field's language. Readers can look these up elsewhere, but your usage may
  be narrower than the general definition; say so where it is.
- **Project-internal terms** — names this project invented: stage names, state fields, pipeline
  concepts, code identifiers that carry meaning. **These exist nowhere else**, which is what makes
  them the higher-value half of this file.

Add a term the first time it is used in a document, not in a cleanup pass later.

## Hard rules

- **Neither folder is written on a general documentation instruction** — see *Write scope*.
  "Document this" covers `Notes/`.
- **`Project_Intent/` is never written without an explicit instruction.** Not on a transition, not
  after a discussion, not "while I was in there".
- **Never create a placeholder.** An absent file means nobody has written it; that is honest.
- **`Key_Decisions.md` and `Project_Timeline.md` are append-only.** Correct an error with a new
  superseding entry, never by editing history.
- **Do not duplicate what lives in `Notes/` or the archives** — link to it. These files are the
  index and the current position, not a second copy of the trail.
- At a phase boundary this skill runs **after** `phase-transition` finishes and **before**
  `phase-context`, so `Key_Decisions.md` exists before `INHERITED.md` links to it. Do the timeline
  and decisions appends first (factual and cheap), then state and understanding (judgment).
- If a fact cannot be verified from a document or a run, mark it unverified rather than asserting
  it. These files become the thing everyone trusts; an unmarked guess here propagates everywhere.
