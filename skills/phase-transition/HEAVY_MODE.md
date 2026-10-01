# Phase Transition — heavy mode

Everything in this file is **heavy mode only**, plus *Completing a deferred summary*, which runs
heavy mode's Step 4 against an archive after the fact.

`SKILL.md` holds light mode, which is the default and is **complete on its own** — nothing here is
needed for a light transition. Read `SKILL.md` first; the step numbers below are its step numbers.

**Never silently upgrade to heavy mode.** If the escape-hatch question in `SKILL.md` suggests it,
recommend it and let the user decide.

## Step 0 (heavy) — which kind of boundary

Settle which kind of boundary this is, because the closeout's emphasis differs:

| Boundary | Meaning | Closeout emphasis |
|---|---|---|
| `clean_break` | This phase ends; next starts on new work | What carried forward, what was abandoned |
| `promotion` | This phase's output becomes the production lineage | What must be ported, what is frozen, **what the receiving side must not re-inherit** |
| `freeze` | Work stops; nothing continues immediately | What state it was left in, what a future reader needs to restart |

## Step 2 (heavy) — the closeout's full nine sections

**Heavy mode — the full nine, in order.** Where a section already exists as `L1`–`L4` from a
light closeout, renumber it to its heavy position and keep its content; never drop one because
its number moved:

1. **What this phase set out to do** — quoted from the earliest plan or `PHASE_CONTEXT.md`, not
   reconstructed from what happened.
2. **What was delivered** — shipped *and* verified. Each line names its evidence. Anything nobody
   verified goes in section 3, not here.
3. **What was not delivered** — including work believed done but never verified. Say which is which.
4. **Decisions still binding** *(light `L1`)*
5. **Carried forward** *(light `L2`)*
6. **Open questions still unanswered** *(light `L3` — a decision the phase needed and never made,
   distinct from a contradiction between two documents)*
7. **Deliberately abandoned** — with reasons. Cheap to write, expensive to lose: without it the
   next phase re-proposes what was already rejected.
8. **Unresolved contradictions** — where two documents disagree and it was never settled. Record
   it as unresolved; do not silently pick a winner.
9. **Unclassified** *(light `L4`)*

Read [EXAMPLE_CLOSEOUT.md](EXAMPLE_CLOSEOUT.md) before writing a heavy closeout — it shows the
sections filled, including the ones that usually get skipped. Fictional content.

## Step 4 — Summarize into `_Summary/`

Write one markdown file per category folder into `Archive/Phase_<NN>-<slug>/_Summary/`:
`Plans.md`, `Architecture.md`, `References.md`, `Discussions.md`, `Backlogs.md` (matching whatever
categories existed). Each must:

- **Trace the chronology of thinking** — walk that folder's documents in date order and show how
  the thinking moved: what was believed first, what changed it, what it settled on. A list of
  titles is not a summary; the value is in the *transitions*.
- **Link every claim back to its source document** by relative path, so the summary maps into the
  evidence beside it rather than replacing it.
- **Record the link map** — which documents supersede, depend on, or answer which others, from
  `companion_docs` / `supersedes` / `depends_on` frontmatter, and from cross-references where
  frontmatter is absent.

Set `summarized: true` in the closeout when done.

## Completing a deferred summary

Triggered by "summarize the Phase 5 archive" or similar, any time after a light transition.

Run **step 4 only**, against `Archive/Phase_<NN>-<slug>/`. Nothing moves, nothing resets, no gates
apply — the archive is immutable and this is purely additive. Then set `summarized: true` in that
archive's `CLOSEOUT.md`.

**Also check step 5c, not only step 4.** It writes into the *current* `Notes/References/`, not
into the archive, so a session that skipped it leaves nothing visible when you are looking at
`Archive/`. Before finishing, look there for `phase-<NN>-archive-index.md` for this archived
phase's number; if it is missing, write it per step 5c too. A closeout that "finishes" without it
leaves exactly what 5c exists to prevent — an archive only its own author can navigate.

If the closeout is also `partial`, offer to fill its remaining sections from the archive at the
same time — flagging clearly that *delivered vs. merely believed done* is being reconstructed
from documents rather than recalled, and marking those entries unverified.
