---
name: notes-discussions
description: >-
  Use when the user asks — in any words — to record, recap or save what was
  discussed or decided, and **whenever a topic that already has a discussion log in
  Notes/Discussions/ is discussed again**: append the new round to that log
  without being asked. Starting a *new* topic log needs the user's go-ahead;
  keeping an existing one current does not. Saves a discussion recap — what was asked, what
  happened, why it was asked, and the agreed steps — as a markdown file with lean
  frontmatter in Notes/Discussions/ instead of only summarizing in chat. Not for the
  forward plan of how to build what was decided — that is `notes-plans`. Not for
  consolidating a whole phase's decisions at a boundary — that is `phase-transition`;
  this skill covers one conversation.
---

# Notes Discussions

When a conversation with the user works through a decision, a vision/requirements ask, or a
change of direction — as opposed to a forward-looking plan (`notes-plans`) or a writeup
documenting *existing* code/data (`notes-references`) — capture the discussion itself:
what was asked, what happened, why it was asked, and what was agreed. Write it to a new file under
`Notes/Discussions/` in addition to summarizing in chat.

## Write scope

Writes only to `Notes/Discussions/`. Never `Project_Intent/`, `Project_Context/`, `Archive/`,
source files, or another `notes-*` folder — each has its own owner. A decision recorded here
often belongs in `Project_Context/Key_Decisions.md` too — that ledger is authoritative and
`project-knowledge` owns it, so say in one line what should be appended and let the user
decide.

**Starting a new topic log needs the user's go-ahead. Keeping an existing one current does not.**

| | Permission |
|---|---|
| **New topic log** | **Ask first.** You cannot reliably tell when a conversation has finished, so don't guess. When a discussion looks worth logging and no file covers that topic, say so in one line and ask. |
| **Existing topic log** | **Append on your own.** No permission needed — see *Appending to a topic log*. |

**Appending is the automatic half, and it is the one that gets forgotten.** When a topic that
already has a log comes up again, add today's round to it then and there. The user will not think
to ask, and a log that stops at round one is worse than none — it reads as the final position on
a question that has since moved.

If `Notes/` isn't scaffolded yet, say so and point at `phase-context`, which owns that — don't
create the tree here. The project's agent instructions may narrow this scope; nothing widens it.

## When to use
- User asks — in any words — to record, recap, or save what was discussed or decided
  ("save this discussion", "recap this", "write down what we agreed", and the like).
- A conversation reaches locked decisions, a stated vision, or a changed direction that should be
  recorded for posterity (e.g. "why did we decide not to do X" needs to be answerable later).
- **A run comparison settles** — enough experiments have been run to pick an approach. Capture
  which won, on what measure, and why; cite the `RUN.md` Result sections of the runs compared
  (see `simple-dev-notebook`/`simple-dev-script` → `RUN.md`) so the decision links to its evidence.
- Not for a forward plan of *how to build something* — use `notes-plans` for that.
- Not for documenting/explaining *existing* files/code/data — use `notes-references`.
- Not for summarizing what a whole **phase** decided — that's `phase-transition`. This skill covers
  one conversation; a closeout consolidates many.
- If the discussion defers work, record the decision here **and** add the item via
  `notes-backlogs` — a deferred item that lives only inside a recap is invisible to
  "what's left".
- A single discussion can still produce a companion plan or reference doc — link them in the
  header rather than duplicating content.

## Timing

**A dated entry records the round that just happened, settled or not.** This is the point of a log
rather than a recap: an entry that says "we narrowed it to two options and did not choose" is a
true record of where the thinking stood that day, and the next entry shows what resolved it.

What must not happen is a decision being written as *locked* when it is not. Record an unsettled
round under *Still open*, not under *Decisions*.

## File naming — deliberately undated

`Notes/Discussions/<topic-slug>.md`
(e.g. `Notes/Discussions/retry-strategy.md`, `Notes/Discussions/empty-report-handling.md`)

**Never put a date in the filename.** One file per topic, grown over time — a date would be wrong
the first time you appended to it. `updated_at` in frontmatter records recency; the dated sections
in the body record the chain.

**One file per topic, and "same topic" is a judgement call.** Before starting a new log, list what
is already in `Notes/Discussions/` and append to an existing file if it is clearly the same
subject. **When it is borderline, ask** — getting this wrong either buries a new question inside
an unrelated log, or splits one subject across two files, which is the problem this structure
exists to prevent.

## Frontmatter

Lean by design — a recap has no priority or effort. Every key below is **required and always
present** (`[]` / `0` when genuinely empty), except `project`, `participants` and `tags` which
are **optional — omit the key if there is no real value.**

```yaml
---
id: "retry-strategy"         # the filename without .md — the topic slug
schema_version: 1
type: "discussion"
title: "Document title"
summary: "One or two sentences — the topic, and where it currently stands."
created_at: "2026-03-04"     # first entry
updated_at: "2026-03-11"     # last entry — bump on every append; the only freshness signal
status: "active"             # active | superseded | archived
supersedes: null             # the archived predecessor, when a topic continues across a phase
                             # boundary — a PATH, not an id, since topic ids repeat per phase
superseded_by: null          # only when a whole topic is replaced by a differently-scoped one;
                             # appending within a topic supersedes nothing
initiative: "Phase 5"        # phase marker — copy verbatim; this is how phase-transition finds the doc
decisions_count: 0           # running total of decisions across all dated entries
backlog_items: []            # ids of any backlog items this discussion created; [] if none
companion_docs: []           # ids of same-topic docs; [] if none
project: "Project Name"      # optional
participants: []             # optional
tags: []                     # optional
---
```

## Content — a standing header, then one section per date

Read [EXAMPLE_RECAP.md](EXAMPLE_RECAP.md) for the shape with two rounds in it. Fictional content.

**Standing header** (rewritten as the topic's understanding changes):

- Title + one line on what this topic covers and where its boundary is.
- `Participants`, `Companion docs` — links to plans, references or backlog items this topic
  produced. Keep current.
- **Where it currently stands** — one short paragraph. The only part a reader skimming needs.

**Then `## <YYYY-MM-DD>` sections, oldest first, newest appended at the bottom.** Each carries
only what applies that day:

- **What prompted this round** — what changed, or what was asked.
- **The ask, as stated** — direct quotes, including refinement rounds. Prefer verbatim over
  paraphrase: future readers need the original intent, not a summary of it.
- **Decisions** — a table, `# | Topic | Decision`, numbered continuously across the whole file so
  decision 4 is always decision 4. When a decision came from comparing runs, name the winning run
  and the measure, and link the compared `RUN.md` files.
- **Why** — rationale for anything non-obvious, especially what reads as surprising or
  restrictive without context. For a run comparison the "why" is the measured result — cite the
  numbers rather than asserting a winner.
- **Still open** — what this round did not settle.
- **Next actions agreed** — concrete follow-ups, in the order agreed.

## Appending to a topic log

**Past dated sections are immutable. Today's is not.**

- **Append a new `## <YYYY-MM-DD>` section** for a new round. Never rewrite an earlier one, even
  when it turned out to be wrong — that it was believed is the record.
- **Editing today's section is fine**, as the day's thinking firms up.
- **A later round that reverses an earlier decision does not delete it.** Add the reversal as a
  new decision that says what it supersedes: *"6. Reverses decision 2 — … because …"*. A log
  that silently rewrote its own history is worth less than no log, because it reads as though the
  project never changed its mind.
- **Bump `updated_at`** on every append, and refresh the standing header's *Where it currently
  stands* if the position moved.

## Notes
- **A new date is not a new file.** Append a dated section to the topic's existing log; a new file
  is created only when the topic itself is new. See *Appending to a topic log* above.
- Keep chat response short; point to the created file rather than repeating it in full.
- If the discussion also produces a plan or a reference writeup, still create those via
  `notes-plans` / `notes-references` and cross-link them under "Companion docs"
  rather than folding their content into the discussion recap.
