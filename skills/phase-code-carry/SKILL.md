---
name: phase-code-carry
description: >-
  Use when the user names it to start the next phase's code from the previous
  phase's — "carry the notebooks into phase 6", "start the next phase from the
  old code", "copy the phase 5 notebooks forward". Copies a phase's code into the
  next phase folder, rewrites its output paths and config so it cannot write into
  the frozen phase's recorded results, verifies the copy by running it, then
  tidies without changing behaviour. **Code only** — `phase-transition` handles
  the notes side of the same boundary, and `research-to-production-port` handles
  code crossing into production. Never edits the source phase.
disable-model-invocation: true
---

# Phase Code Carry

Notes get archived at a phase boundary; **code does not.** The previous phase's folder stays
exactly where it is and must keep working. The next phase starts from a *copy* — never an import,
because importing across phases means the older one can never be changed or frozen again.

This skill runs that copy, in three stages that must not be merged.

## Prime directive: the previous phase still runs, and still produces what it produced

Everything here is additive. Nothing in `research_repository/Phase_<NN>-<slug>/` — the source phase — is
edited, moved or deleted. If a step would require touching the source, stop: that is no longer a
carry, it is an edit to a frozen phase, and it invalidates the closeout that cites its results.

**If this project's phase code doesn't live under `research_repository/`, translate before you
start — the stages don't change, only the paths do.** Read "the source phase folder" as wherever
the previous phase's code actually lives, "the target phase folder" as its next-phase equivalent,
and Stage 2's grep target — "the old phase's slug" — as that source folder's own name, slug or
not. Every stage and hard rule below then applies as written.

---

## Stage 1 — Copy

Copy from `research_repository/Phase_<NN>-<slug>/` into `research_repository/Phase_<NN+1>-<slug>/`.

**Carry nothing unless it is named.** The default is exclusion, not inclusion. Ask which
notebooks are coming across, and leave behind:

- dead experiments and superseded notebooks
- scratch files, one-off checks, anything that ran once
- `lib/` or `utils/` code the carried notebooks do not actually import

Copying everything means the new phase begins in debt, and nobody deletes later what looked
deliberate on arrival.

**A file whose use isn't obvious from its name or location is not a guess — check first.** Before
asking whether a large or ambiguous data file is carried, grep the notebooks being brought across
(and anything they import) for it. Ask armed with the answer — "nothing carried touches this
file", or "the cleaning notebook reads it directly" — not with the bare question.

**Renumbering.** If stages are dropped or added, the numbers shift — and the number *is* the
run-order contract. Renumber into a clean sequence, and record the old-to-new mapping in the new
phase's `README.md`. A number that silently means something different from last phase is worse
than a gap.

## Stage 2 — Rewrite paths and config, then verify

**This is where the damage happens if it is skipped.** A copied notebook still points at
`research_repository/data/Phase_<NN>-<slug>/`. Run it unchanged and it writes into the **previous** phase's
run folder — polluting results the closeout cites as evidence, inside a phase that is supposed to
be frozen. Silent, and it corrupts the one thing archives exist to protect.

### 2a — Rewrite paths and config

Check each of these against the actual code — rewrite what needs it:

- every output path → `research_repository/data/Phase_<NN+1>-<slug>/`
- any hardcoded phase name or slug in strings, config or file paths
- relative imports that reach outside the new phase folder

**"Verified, nothing needed rewriting" is a legitimate outcome, distinct from "rewrote it" —**
some projects resolve their working directory at runtime and hardcode nothing. That's not a sign
this step was skipped, as long as it was actually checked.

**Then grep the new folder for the old phase's slug regardless of what the check above found.**
Zero hits, or you are not done — an explicit check, not an assumption, and it still applies when
nothing needed rewriting.

**Config staleness.** Values tuned for the previous phase carry across silently and look
deliberate. Go through the copied `config.py` line by line with the user and mark what is a
genuine starting point versus a leftover. A stale value that looks intentional is worse than a
missing one.

### 2b — Verify by running

**Verify before touching logic.** Run the carried notebooks once. They should produce output
matching the source phase's last run, in the *new* data folder. That match is what makes stage 3
safe — you now know the copy is faithful, so anything that changes afterwards changed because you
changed it.

## Stage 3 — Tidy, without changing behaviour

Only now, and only while output still matches. Use `refactoring` for this stage: extract, rename,
delete dead branches, reduce duplication — **behaviour identical throughout**, verified against
the stage 2 baseline.

Doing the tidy here rather than later is the whole point. Once the new phase starts changing
behaviour on purpose, you can no longer tell a tidy-up bug from an intended change.

## Then stop

**Everything after stage 3 is the new phase's work, not this skill's.** `refactoring` no longer
applies the moment behaviour is meant to change — a new phase exists precisely because something
should work differently, and calling it a refactor at that point either blocks the work or
redefines the word.

Hand back with what carried, what was left behind, and what stage 2 flagged as stale.

## Related

- **`document-code-comments`** — the carried notebooks' module headers now describe the previous
  phase. Worth updating, but it edits source: **offer it; do not run it** unless asked.
- **`phase-transition`** owns the notes side of the same boundary — it archives `Notes/`, this
  skill touches only `research_repository/`. Neither calls the other.
- **`research-to-production-port`** — crossing into production is a different job with a
  different quality bar, and it ports one named run rather than a phase folder. Not this skill.

## Hard rules

- **Never edit, move or delete anything in the source phase.**
- **Never import across phases.** Copy, or the older phase can never be frozen.
- **Never run a carried notebook before stage 2a's grep passes clean.**
- **Never merge stages 2 and 3.** A tidy applied before the copy is verified cannot be told apart
  from a copy that was wrong.
- **Carry nothing that was not named.**
