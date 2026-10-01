---
name: project-state-brief
description: >-
  Use at the start of a session or when the user asks where things stand -
  "where are we", "catch me up", "what's the current state", "read the notes
  and tell me what's going on", "what should I work on next". Answers from the
  project's own Notes trail in a fixed cheap read order, and flags staleness and
  contradictions instead of smoothing them over. Read-only: writes nothing
  unless asked. Not for documenting code or data (use
  `notes-references`), and not for a phase boundary (use
  `phase-transition`).
---

# Project State Brief

Answers "where are we" without reading the whole `Notes/` tree. The trail grows without bound;
the answer should not get more expensive every week.

## When to use
- Session start on an ongoing project, or any "catch me up" / "what's next" question.
- Before planning new work, so the plan starts from current state rather than assumption.
- Not when the user asks about one specific document — just read that one.
- Not at a phase boundary — that's `phase-transition`, which writes.

## Machine check — run this first

`scripts/validate_notes.py` ships **with this skill**. The project being examined does not have to
contain it, and nothing needs to be copied into the project to make it work — the script takes the
project root as an argument. Run it before the read order.

**Find it, then run it.** Harnesses differ in whether they tell you where a loaded skill's files
live, so there are two routes and the second always works:

1. **If this skill's base directory was reported when it loaded, use it.**

   ```
   python3 <that directory>/scripts/validate_notes.py <project-root>
   ```

2. **Otherwise search the install roots.** Never guess a path, and never look for the script
   inside the project being examined — it is bundled with the skill, not installed per project.

   ```
   find ~/.agents ~/.claude ~/.codex ~/.copilot ~/.cursor \
        .agents .claude .github .cursor -maxdepth 8 \
        -path '*project-state-brief*' -name validate_notes.py 2>/dev/null | head -1
   ```

   Take the first hit and run it with the project root as the argument. The roots vary by harness
   and may be extended; the constant is the tail `project-state-brief/scripts/validate_notes.py`,
   so widen the root list rather than changing what you match on.

3. **If neither route finds it, say so in one line and continue** with the read order. It is
   bundled, so absence means an incomplete install — not a project that never had it.

It checks what prose can't enforce and a phase boundary later pays for: a document with no
frontmatter or no `initiative` (invisible when the phase is archived), a duplicate backlog ID, a
`next_item_id` that is too low, loose prose in a backlog file, an item that was open in the last
archived backlog and reached no current one. Fold every **ERROR** into the brief under *Flag,
don't smooth* — verbatim, with its file — and give the WARN count.

If it errors out, or the tree predates this library (many "no frontmatter" lines on legacy files),
say so in one line and continue with the read order. **Never block the brief on it, and never fix
what it reports** — this skill is read-only.

This is the one place the validator is wired in: cheap here, since the brief already reads the
tree, and it catches "a skill didn't do what its body said" while someone is about to act on the
state rather than at the boundary, where the same defect costs the most.

## Read order (stop as soon as the question is answered)

0. **`Project_Intent/Project_Overview.md`** — what we are building. The entry point; skip only if
   you have already read it this session.
1. **`Project_Context/Project_State.md`** — where we are now. Check its `last_updated_at_phase`
   against the current phase first (see staleness below).
2. **`Project_Context/System_Understanding.md`**, then **`Notes/PHASE_CONTEXT.md`** and
   **`Notes/INHERITED.md`** — how the system currently works, what this phase is, what it inherited.
3. **The active backlog files** in `Notes/Backlogs/` — current open work, by construction.
4. **The most recent `Archive/*/CLOSEOUT.md`** — the position at the last boundary. This replaces
   reading anything older than it. Note its `closeout:` and `summarized:` fields — a `partial`
   closeout means sections were deferred, so treat its silence as *not yet written*, never as
   *nothing to report*.
5. **The archive index** in `Notes/References/*-archive-index.md`, if one exists — what the
   previous phase documented and decided, and where it sits. Use it to locate a document or
   recall a decision; `Key_Decisions.md` remains authoritative for what still binds.
6. **The two or three most recently updated topic logs** in `Notes/Discussions/` — ordered by
   `updated_at`, **not** by filename, which carries no date. Read each log's standing header
   first; the dated entries below it are the chain, and you usually only need the newest.
7. **Open questions from the most recent plans** — those sections only, not whole plans.

8. **Only if the question is "what have we tried?"** — the run index,
   `Notes/References/*-experiments.md`. Read the *Current best* line and the `Outcome` column; do
   not open run folders. This is the only step that touches experiment history, and it is skipped
   unless asked for, because most briefs do not need it.

Only go past step 8 when a specific gap demands it, and say which document you had to open and
why. Reading everything is the failure mode this skill exists to prevent.

## Staleness check (run this every time)

Compare `last_updated_at_phase` in each `Project_Context/` file against `initiative` in
`Notes/PHASE_CONTEXT.md`. **Any KNOWLEDGE file behind the current phase is stale by definition —
report it by name before answering from it.** This is the check that catches a project summary
drifting out of date before someone acts on it.

`last_updated_at_phase: "Seeding Phase"` is the exception — `project-knowledge`'s sentinel from
`initialize`, before any phase existed. **Not stale.** Report it as "seeded, not yet
phase-updated", never as a staleness finding.

## What to report

- **Current phase / focus**, and its stated goal.
- **What landed recently** — with the evidence (run, commit, verification doc), not just claims.
- **What is open** — top backlog items by priority, with IDs.
- **Decisions that constrain what happens next**, with links.
- **Open questions nobody has answered** — these are usually the actual blockers.
- **What you did not read**, in one line, so the user can tell how complete the picture is.

## Flag, don't smooth (the part that earns this skill)

Report these explicitly rather than writing a tidy narrative over them:

- **Machine-check errors** — every ERROR from `scripts/validate_notes.py` (see *Machine check*
  above), verbatim, with its file. These are structural defects a reader would otherwise hit at
  a phase boundary, where they cost the most.
- **Staleness** — a document whose content is contradicted by a newer one, or whose file date is
  far behind the rest of the trail. Name it and say what it still asserts.
- **Contradictions** — two documents disagreeing on scope, naming, or status. Present both and
  say which is more recent; do not pick a winner silently.
- **Naming drift** — the same work referred to by different phase names, stage names, or paths.
- **Unverified claims presented as settled** — especially anything marked as certain or complete
  that no run, commit, or verification document backs.
- **Deferred archive work** — any `Archive/*/CLOSEOUT.md` with `summarized: false` or
  `closeout: partial`. Mention it once, with the phase name, so the debt stays visible; running
  `phase-transition` against that archive completes it.
- **Intent vs. context divergence** — where `Project_Context/System_Understanding.md` now
  contradicts `Project_Intent/Technical_Specifications.md`, or the built system has drifted from
  `Project_Overview.md`'s stated scope. **Report it; never reconcile it.** Intent files are
  user-owned and only they decide whether reality or the spec should move. A stale-looking
  `last_updated_at_phase` on an intent file is normal and is not itself a finding.

A brief that reads as coherent while resting on a stale document is worse than one that reports
the mess, because the user acts on it.

## Output

Answer in chat by default — this runs often, and a dated file per run would itself become
clutter. **Nothing is written unless the user explicitly asks for a file.** When they do, write
it to `Notes/References/project-state-brief.md` following `notes-references`' frontmatter —
**appending a dated entry** rather than creating a new file, so repeated briefs become one log
rather than a pile of near-identical snapshots.

Keep it scannable and short enough to actually read: the point is to replace a long read, not
relocate it.

## Notes
- Never state project state from memory or from earlier in the conversation — read the trail.
  Stale recall is exactly the failure this skill prevents.
- If `Notes/Backlogs/` and `Archive/` do not exist yet, fall back to reading the dated document
  folders directly (`Notes/Plans/`, `Architecture/`, `References/`, `Discussions/` — or whatever
  this project called them before adopting these names). Say that the read was more expensive as a
  result, and mention that `notes-backlogs` and `phase-transition` would make future briefs cheap.
- **A folder the validator reports as unrecognised has had nothing inside it checked** — not just
  its name. Read those documents yourself before relying on them, and say in the brief that they
  are unvalidated.
