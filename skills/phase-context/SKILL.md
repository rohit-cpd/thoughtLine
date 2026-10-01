---
name: phase-context
description: >-
  Defines the phase currently in flight — owns Notes/PHASE_CONTEXT.md and
  Notes/INHERITED.md, and scaffolds Notes/ on first use. Name it to start a phase,
  change its scope or focus, or ask what this phase is about or what it inherited
  ("start phase 6", "narrow the scope of this phase", "what did we inherit"). Not
  for the first-time project scaffold — that is `project-start`.
disable-model-invocation: true
---

# Phase Context

Owns the two files that sit at the root of `Notes/` and describe the phase currently in
flight. Everything else in `Notes/` is produced by the `notes-*` skills; these two are the
frame around them.

## Write scope

**This skill runs only when the user names it** — to start a phase, change its scope, or ask what
this phase is about. Starting or redefining a phase is not something to infer from a conversation
drifting onto new work; if that seems to be happening, say so in one line and wait.

Writes `Notes/PHASE_CONTEXT.md` and `Notes/INHERITED.md`, and scaffolds the empty `Notes/`
category folders. Never writes documents *into* those folders, and never writes
`Project_Intent/`, `Project_Context/`, `Archive/` or source files. The project's agent instructions
may
narrow this scope; nothing widens it.

## Files owned (only these two)

| File | Nature | Who writes it |
|---|---|---|
| `Notes/PHASE_CONTEXT.md` | Authored, updated as the phase moves | This skill, with the user |
| `Notes/INHERITED.md` | **Derived** from the previous phase's `CLOSEOUT.md` | This skill, never by hand |

## Step 0 — Make sure `Notes/` is ready

Two ways you arrive here, and they need different things:

**After a `phase-transition`** — `Notes/` already holds the five empty category folders and the
carried-forward backlog files. Nothing to scaffold. Write the two root files and stop.

**Cold start** — no `Notes/` at all, or no category folders inside it. Create them:

```
Notes/
├── Plans/
├── Architecture/
├── References/
├── Discussions/
└── Backlogs/
```

**Before scaffolding a fully empty `Notes/`, check for a just-created `Archive/` folder with no
matching evidence in `Notes/`** — no carried-forward backlogs, no archive index. That pairing is
`phase-transition` having moved the tree (Step 3) and stalled before Step 5, not a cold start:
tell the user to resume `phase-transition` at Step 5 rather than scaffolding here.

### Guard: never scaffold over an unarchived phase

If `Notes/` already contains documents *and* a `PHASE_CONTEXT.md` for a different phase than the
one being started, **stop.** That is a previous phase that was never archived, and writing a new
`PHASE_CONTEXT.md` over it silently merges two phases into one folder — after which no boundary
can separate them again. Tell the user to run `phase-transition` first.

The safe cases are: `Notes/` absent, `Notes/` holding only empty folders, or `Notes/` holding
only what a transition that just ran leaves behind — carried-forward backlog files in `Backlogs/`
**and** the archive index step 5c writes to `References/phase-<NN>-archive-index.md`. That index
is a document, so name it explicitly: those two and nothing else is a clean post-transition
state, not an unarchived phase.

## Phase identity and goal — settle these together

Phase naming drifts silently: the same work ends up called "Phase 5" in one document, a letter
or codename in another, and a folder path in a third. Before writing `PHASE_CONTEXT.md`, pin
down and record all four of these, asking the user where ambiguous:

- **Number** — zero-padded two digits (`05`, `06`) so directory sorting survives past nine
- **Slug** — short kebab-case, e.g. `notebook-pipeline`
- **Canonical name** — what a human calls it, e.g. `Phase 6 — Production Port`
- **Aliases** — every other name this work appears under in older documents
- **`initiative`** — **derived, not chosen:** the literal string `Phase `, then the number with
  leading zeros stripped. `phase_number: "06"` → `initiative: "Phase 6"`. Never a codename, never
  the slug, never the canonical name — those go in `aliases`.

**Why it is derived rather than named.** It is the most load-bearing string in the system: every
document the `notes-*` skills write carries it verbatim, and one that doesn't is invisible when
the phase is archived — so a free-form string, once propagated by copy, cannot be corrected
without re-tagging every document in the phase. Derived from the number it is reproducible, and
the validator bundled with `project-state-brief` can check the derivation instead of taking it on
trust. A project with a real reason to use something else should put the human-facing name in
`aliases` and expect the validator to flag the `initiative` every run.

**Settle the goal first; the slug names the scope, so a slug agreed before the goal will
contradict it.** Get the one-line goal, then the slug, then check them against each other before
writing anything — they describe the same phase from two angles, and if they point different
directions one of them is wrong. Ask then and there, while it is still two answers in the
conversation rather than two lines in a file:

> *You said the goal is "continue the old backlog", but the slug you gave — `payments-v2` —
> names new scope. Is this phase finishing carried-over work, or starting something new?*

Gathering the goal later, in the sections step, costs an extra round and briefly records a
contradiction.

The archive folder for this phase will be `Archive/Phase_<NN>-<slug>/`. Fix the number and slug
now so `phase-transition` does not have to invent them later.

## `Notes/PHASE_CONTEXT.md`

```yaml
---
id: "phase-06-context"
schema_version: 1
type: "phase_context"
title: "Phase 6 — Production Port"
phase_number: "06"
phase_slug: "production-port"
initiative: "Phase 6"        # the exact string every doc in this phase must carry
aliases: []
status: "active"             # active | closing | closed
started_at: "2026-09-01"
last_updated: "2026-09-01"
previous_phase: "Phase 5"
---
```

Sections:

1. **Goal** — one paragraph, in terms of the outcome, not the tasks. Expand the one-line goal
   already settled above and checked against the slug; do not re-derive it here.
2. **In scope / out of scope** — an explicit two-column boundary. The out-of-scope column is
   the one that earns its keep: it is what stops work sprawling mid-phase.
3. **Current focus** — what is being worked on right now. This is the only section that changes
   often; update it as the phase moves rather than letting it describe week one forever.
4. **Success criteria** — how you will know this phase is done. Written at the start, not
   reverse-engineered at the end from whatever happened.
5. **Open questions** — decisions this phase needs that have not been made yet. At the boundary,
   `phase-transition` copies whatever is still unanswered here into the closeout and the archive
   index. Keep it current: add one when it arises, strike one the moment it is decided (recording
   the decision via `notes-discussions` / `project-knowledge`).

   This is the **primary** carry path, not the only one — `phase-transition` L3 also sweeps the
   *Still open* entries in `Notes/Discussions/` logs. That is not a reason to skip this section:
   it is the one place a question is visible *during* the phase rather than only at its end.

State the `initiative` string plainly in the file, so every document in the phase can copy it
verbatim — that is how `phase-transition` finds them at the boundary.

## `Notes/INHERITED.md` — derived, never hand-edited

Generated from the previous phase's `Archive/Phase_<NN>-<slug>/CLOSEOUT.md`. Its job is to put
last phase's handoff in the current working set instead of leaving it buried in an archive.

Open the file with this line verbatim, so nobody edits it and creates a third version of the
truth:

> *Derived from `Archive/Phase_05-.../CLOSEOUT.md`. Do not edit by hand — regenerate instead.*

Sections:

1. **What the previous phase delivered** — one short list, each item linking into the archive.
2. **Carried forward** — open backlog items that moved into this phase, by their original IDs.
3. **Constraints that still bind** — **link to `Project_Context/Key_Decisions.md`; do not restate
   the decisions here.** That ledger is authoritative and cumulative; a copy here would drift.
   Two gaps to handle, and never by linking to a file or a row that isn't there:
   - **No ledger yet** (first boundary, or `project-knowledge` has not run) — link to the
     closeout's *Decisions still binding* section and say the ledger is not yet established.
   - **Ledger exists but is incomplete** for this phase's newest decisions — open it and confirm
     each row before linking to it, rather than taking the closeout's citation on trust. For a
     decision the closeout calls binding that isn't in the ledger yet, link to that one closeout
     section and say "not yet appended" — `phase-transition`'s wording for the same gap, so a
     reader meets one phrase for this state, not two.
4. **Deliberately abandoned** — what the previous phase rejected and why, so this phase does not
   re-propose it.
5. **Known unresolved contradictions** — carried across verbatim, still unresolved.
6. **Open questions inherited** — the previous closeout's *Open questions still unanswered*
   section, verbatim. Decisions the last phase needed and did not make; this phase either makes
   them or carries them on again. If any is already in scope for this phase, say so next to it.

If there is no previous phase, or no closeout for it, write `INHERITED.md` anyway with a single
line saying so. An absent file is indistinguishable from a forgotten one.

`INHERITED.md` has **no frontmatter** — it opens with the "Derived from…" line above.
`phase-transition` knows this and never flags it as an unattributed document; do not add a YAML
block to make it look like the other notes.

## Worked example

Read [EXAMPLE_PHASE_CONTEXT.md](EXAMPLE_PHASE_CONTEXT.md) to see both files as they look at the
start of a phase, immediately after the previous one was archived — including a derived
`INHERITED.md` that links to the decisions ledger instead of restating it. Fictional content.

## When to update

- **Phase start** — scaffold if needed (step 0), then both files, `INHERITED.md` first (it
  informs the scope).
- **This skill covers the notes side only.** If the new phase starts from the previous phase's
  code, that is a separate operation — `phase-code-carry` copies the notebooks forward, rewrites
  their paths, and verifies the copy before anything is changed. Mention it at phase start;
  do not run it.
- **First phase of a brand-new project** — there is no closeout to derive from. Write
  `INHERITED.md` with a single line saying this is the first phase, and consider suggesting
  `project-knowledge` in `initialize` mode so `Project_Context/` exists before the phase
  produces anything worth recording there.
- **Scope changes mid-phase** — update `In scope / out of scope` yourself; that part is this
  skill's own file. *Why* it changed belongs in `notes-discussions`, a separate skill's document:
  **ask, don't write it as an automatic second step** — and don't skip it silently either, since
  the reason is what future-you cannot reconstruct. *"Want me to record why the scope changed, as
  a discussion note?"*
- **Focus shifts** — update `Current focus` only. Cheap, frequent, low ceremony.
- **Never** rewrite `Goal` or `Success criteria` to match what actually happened. If they turned
  out wrong, say so in the closeout at the boundary. Editing them retroactively erases the
  evidence that the phase drifted.

## Hard rules

- Scaffolding empty folders is in scope; **populating them is not.** Documents inside
  `Notes/Plans/`, `Architecture/`, `References/`, `Discussions/` and `Backlogs/` belong to the
  `notes-*` skills.
- Two files, no more. New categories of phase state belong in the `notes-*` folders.
- Bump `last_updated` on every edit.
- Do not track open work here — that is `notes-backlogs`, which owns itemized state with stable
  IDs. A second list of open items in `PHASE_CONTEXT.md` would drift from the backlog within days.
