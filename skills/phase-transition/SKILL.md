---
name: phase-transition
description: >-
  Runs a phase boundary: archive Notes/ into Archive/, carry open backlog items
  and open questions into the next phase, reset Notes/, write a closeout. Light by
  default; heavy ("full closeout") on request. Name it to "close out phase 5",
  "archive this phase", "move to the next phase", or to finish a deferred archive
  summary later. **This is about ending a whole phase, not about deferring one
  piece of work** — an individual item moving to a later phase is
  `notes-backlogs`. Not for a status check or "where did we land" — that is
  `project-state-brief`.
disable-model-invocation: true
---

# Phase Transition

A phase boundary is the one moment an append-only notes trail fails: it records every step but
never states the resulting position. This skill moves the phase's work into a permanent archive,
carries what is still open into the new phase, and leaves `Notes/` empty.

## Two modes — light is the default

|  | **Light** (default) | **Heavy** (on request) |
|---|---|---|
| Closeout | 4 sections | 9 sections |
| `_Summary/` chronologies | Deferred | Written now |
| Boundary type | One yes/no question | Full taxonomy |
| Cost on a large phase | Minutes | An hour or more |

**Run light unless the user asks for a full closeout, or the escape-hatch question below says
otherwise.** Most boundaries do not need the heavy treatment, and a procedure heavy enough to
dread is a procedure that gets skipped.

### Why deferring the summary is safe

Sort the steps by what happens if you skip them:

- **Irreducible** — move the tree, carry the backlog, reset `Notes/`. Skip these and the phase
  does not actually end.
- **Degrades if deferred** — the closeout. Which items were *verified* versus merely believed
  done, and *why* something was rejected, live in the user's head right now and nowhere else.
  Reconstructing that later is possible but lossy. So light mode still writes a short one.
- **Free to defer, permanently** — `_Summary/`. Its only input is the archive, and the archive is
  immutable. Generating it next week yields exactly the same result as generating it today.

That is the whole basis for light mode: the most expensive step is the one with no deadline.

### The escape hatch (ask this in light mode)

> *Is any of this phase's work being ported into another lineage — code moving to a different
> codebase, a prototype becoming production?*

If **yes**, recommend heavy mode before continuing. What the receiving side must **not**
re-inherit — bugs already fixed here, decisions that do not travel — is exactly what a short
closeout omits, and it is unrecoverable once the port has happened.

## Prime directive: `Notes/` must end up empty

Every document leaves `Notes/` and lands in `Archive/`. Achieve that by **moving** the tree — not
by copying it and then deleting the originals.

Move is a single operation: the archive *is* the original, there is no second copy to verify, and
no window in which a partial copy is followed by a successful delete. Copy-then-delete opens
exactly that window, and it is unrecoverable when it does.

### If `mv` is genuinely unavailable

Some environments permit `mv` but block `rm` by design. If moving fails: copy the tree, **verify**
that file count and per-file byte sizes match the step 1 inventory plus `CLOSEOUT.md`, then
request permission to remove the originals — removing only paths you verified. If permission is
refused, **stop and tell the user** which files now exist in both places; never leave a
half-cleared `Notes/` silently. This is the only removal this skill may ever perform.

---

## Step 0 — Identity  · *light + heavy*

If `Notes/PHASE_CONTEXT.md` exists, take `phase_number`, `phase_slug`, `initiative` and `aliases`
from it. Otherwise ask, and record what you were told. Also settle the **next** phase's
`initiative` string — step 5 stamps the carried-forward backlog with it, and `project-knowledge`
reads it from this closeout during the window where `PHASE_CONTEXT.md` does not yet exist.

`next_initiative` is **derived, not invented**, by the same rule `phase-context` uses: the literal
string `Phase `, then the next phase number with leading zeros stripped — `05` here gives
`Phase 6`. Never a codename or the next phase's slug. It is copied verbatim onto every document
the next phase writes, so correcting it later means re-tagging all of them.

Archive folder name is deterministic, never AI-invented: `Archive/Phase_<NN>-<slug>/`

**Light:** ask the escape-hatch question above; record `boundary_type: null` unless it promoted
you to heavy.

**Heavy:** settle which kind of boundary this is — `clean_break`, `promotion` or `freeze` —
because the closeout's emphasis differs. The taxonomy is in
[HEAVY_MODE.md](HEAVY_MODE.md).

## Step 1 — Inventory, tolerating legacy layouts  · *light + heavy*

`Notes/` will not always match the current convention. Map what you find; **report anything you
cannot map rather than silently moving on**:

| Found | Action |
|---|---|
| `Plans/`, `Architecture/`, `References/`, `Discussions/`, `Backlogs/` | Current names — move as-is |
| A folder that plays one of the five roles above but under an **older name this project used** — whatever it was called before adopting these names | Legacy name — **move it under its original name; do not rename on the way in.** Renaming breaks the relative links inside the documents (`../<the-old-name>/...`), which stay valid only if the tree moves intact. Record the old-name → category mapping in the closeout, or nobody will know what that folder was |
| Any other folder (e.g. `Files/`, `Plan/`) | Move as-is; list under *Unclassified* in the closeout |
| Any project-wide summary document (`PROJECT_SUMMARY.md`, `OVERVIEW.md`, `STATUS.md` — whatever this project called it) | Move it, **but tell the user it should seed `Project_Context/Project_State.md`** when they run `project-knowledge` — otherwise it is archived into oblivion |
| Missing `PHASE_CONTEXT.md` / `INHERITED.md` | Proceed. Reconstruct what you can and mark it *inferred, not authored* |
| `INHERITED.md` and `CLOSEOUT.md` themselves | Framework files, not phase documents. `INHERITED.md` has **no frontmatter by design**; `CLOSEOUT.md` carries its own. Move as-is. **Never** count either as "unattributed" or list it in the ask below. |
| A **few** category documents (roughly ≤5 in a folder) with no frontmatter or no `initiative` | Cannot be phase-attributed automatically. **List these and ask** — never guess |
| **Most or all** documents in a folder have no frontmatter (a tree that predates this library) | Do **not** ask per file — that is dozens of questions. Attribute the whole folder to this phase from its position in the tree and the documents' own dates, **state plainly what you attributed and on what basis**, and ask the user to confirm the batch in one question. Flag any single file whose date sits well outside the rest as a possible outlier. Record `documents_unattributed` as the count you batch-attributed. |
| A `Backlogs/` file with text outside a `### <ID> — <title>` item (loose paragraphs, a "misc" / "housekeeping" section) | Every such task must carry forward. **Mint continuation IDs from that file's `next_item_id`**, one per distinct task, before step 5b runs, and note the mint in the closeout's *Carried forward*. Never carry it as prose; never drop it. |

Record the exact file count and path list — step 3 verifies against it.

## Step 2 — Write `CLOSEOUT.md` into `Notes/`  · *light + heavy*

Write it into `Notes/` first, before anything moves, so it can be reviewed while every source
document is still in place. It travels with the tree in step 3.

```yaml
---
id: "phase-05-closeout"
schema_version: 1
type: "phase_closeout"
title: "Phase 5 — closeout"
summary: "One or two sentences."
date: "2026-09-01"
phase_number: "05"
phase_slug: "notebook-pipeline"
initiative: "Phase 5"
aliases: []
boundary_type: null          # null in light mode; set in heavy
next_initiative: "Phase 6"
mode: "light"                # light | heavy
closeout: "partial"          # partial (light) | full (heavy)
summarized: false            # true once _Summary/ exists
documents_inventoried: 0     # count of documents read/moved by this closeout, of any kind.
                              # Same number step 3 verifies against; excludes CLOSEOUT.md itself
                              # and anything under _Summary/.
documents_unattributed: 0    # count of *documents* (not folders) batch-attributed under Step 1's
                              # "most/all lack frontmatter" rule, without per-file confirmation.
                              # NOT the §9 "Unclassified" list — those couldn't be attributed at
                              # all and are listed there instead, never counted here.
---
```

**Both counts are checked** against the archive itself by the validator bundled with
`project-state-brief` — get them wrong and the next brief says so.

**Light mode — four sections only.** They are numbered **L1–L4**, not 1–4, so they never collide
with the heavy nine below. A light closeout later completed into a heavy one keeps every section
it already had — the letters make the mapping obvious (L1→4, L2→5, L3→6, L4→9) instead of
requiring a renumber, which is where a section quietly gets dropped.

- **L1. Decisions still binding** — each with a one-line why and a link to where it was made. This
  is what stops the next phase re-litigating settled questions or silently violating them, and
  it is the one thing that genuinely decays if you put it off. If citing a decision that should
  already be in `Project_Context/Key_Decisions.md`, **open the ledger and confirm the row is
  actually there before treating it as recorded** — a decision made in this phase's final days is
  often not yet appended, since `project-knowledge` runs *after* this skill, at the hand-off in
  Step 6. If it isn't in the ledger yet, say so plainly: "not yet appended to `Key_Decisions.md`
  — cite from `<the discussion or plan that made it>` until `project-knowledge` runs." Don't
  imply ledger presence for a decision only this closeout has recorded so far.
- **L2. Carried forward** — the **travelling set**, by ID and source area file. Step 5 writes
  these into the new backlog, so an item missing here is an item lost. **Enumerate it from the
  backlog files, never from recall or from the conversation** — open every file in
  `Notes/Backlogs/` and take:
  - every item whose `Status:` **keyword** (the text before the first ` — `) is `open`,
    `in-progress` or `blocked` — ignore any short note after the dash;
  - every item whose keyword **is not one of the six** — legacy prose like "known bug,
    unfixed". That means *carry it, and flag it for a real keyword*, **never** *no match, so
    drop it*;
  - every task minted an ID in step 1 because it was loose prose in a backlog file.

  Record the per-file count. `done`, `dropped` and `superseded` items are not in the set — they
  stay in the archived file; that history is the archive's job.
- **L3. Open questions still unanswered** — this is the only carry path an open question has:
  they are not backlog items, and `INHERITED.md` is derived from this closeout, so a question left
  out here is one the next phase never sees. **Gather from three sources, not one** — a
  hand-maintained list is exactly the thing that goes out of date:
  1. The *Open questions* section of `PHASE_CONTEXT.md`, verbatim.
  2. **Every unresolved *Still open* entry in `Notes/Discussions/`.** A topic log records what each
     round did not settle; if a later entry in the same log answers it, it is resolved and does not
     carry. This source exists precisely because nobody reliably remembers to also add the question
     to `PHASE_CONTEXT.md`.
  3. Any still-open question in the phase's plans.

  **De-duplicate across the three and say where each came from**, so a question that only ever
  existed in a discussion log is visibly not a `PHASE_CONTEXT.md` omission to be scolded about
  later. Omit the section only if all three sources are genuinely empty.
- **L4. Unclassified** — folders and documents that did not map to a category, by path. Omit if empty.

Open the body with one line stating the debt, so it is visible to anyone who opens the archive:

> *Light closeout — sections L1–L4 only. `_Summary/` not written and the heavy-only sections
> (what the phase set out to do, what was and wasn't delivered, deliberately abandoned,
> unresolved contradictions) not filled — run `phase-transition` against this archive to
> complete them.*

**Heavy mode — the full nine sections** are in [HEAVY_MODE.md](HEAVY_MODE.md), together with the
`L1`–`L4` → heavy mapping.

> ### GATE 1 — stop here
> Show the closeout and the planned archive path. **Nothing moves until the user approves.**
>
> **A gate does not persist across other work.** If any other skill runs, or the user changes
> topic, before this gate is answered, treat it as expired — re-show the closeout and the
> planned path and ask again. An approval that arrives after unrelated work is not consent to
> what you showed twenty minutes ago; the state it was based on may have moved.

**This gate is self-evidencing — use it.** `Notes/CLOSEOUT.md` present and unmoved *is* the
record that Gate 1 was shown and not approved. Check for it before drafting: if it is there, this
is a **resumed** run — re-show that closeout and the same archive path and ask again. Never draft
a second closeout beside the first.

## Step 3 — Move `Notes/` into the archive  · *light + heavy*

Move every folder and file from `Notes/` into `Archive/Phase_<NN>-<slug>/`, preserving internal
structure exactly. `CLOSEOUT.md` lands at the root of that folder.

Verify: the archive contains **everything the step 1 inventory listed, plus the one `CLOSEOUT.md`
written in step 2** — that is `inventory_count + 1` files — and `Notes/` is empty. **If the counts
disagree, stop and report.**

## Step 4 — Summarize into `_Summary/`  · *heavy only*

**Light mode skips this entirely** and leaves `summarized: false` — safely, for the reason in
*Why deferring the summary is safe* above. The procedure is in
[HEAVY_MODE.md](HEAVY_MODE.md), and can be run against the archive at any later date; see
*Completing a deferred summary* there.

> ### GATE 2 — stop here
> Everything so far is additive; the archive exists and nothing is lost. **Step 5 resets
> `Notes/`.** Show what will be recreated and which backlog items carry forward, then get an
> explicit go-ahead.
>
> **Same staleness rule as GATE 1** — and it matters more here, because Step 5 is destructive to
> `Notes/`: if other work intervened, re-show the plan and the carry-forward list, and ask again.

**This gate is also self-evidencing.** By this point `Notes/` is empty and
`Archive/Phase_<NN>-<slug>/` already holds the moved tree — that combination, on its own, is the
record that Gate 2 was reached and Step 5 never ran. Before starting a *new* transition, check
for it: an empty `Notes/` with a just-created archive folder is a stalled Step 5, not a clean
starting point. Resume at Step 5; don't re-run Steps 0–4 against an archive that already exists.

## Step 5 — Reset `Notes/`, carry the backlog forward, index the archive  · *light + heavy*

**5a. Recreate the empty structure:**

```
Notes/
├── Plans/
├── Architecture/
├── References/
├── Discussions/
└── Backlogs/
```

Use the current names regardless of what the archived phase used — the rename takes effect from
this phase forward, and the archive keeps its original names.

**5b. Carry open backlog items into the new phase.** This is the one file another skill normally
owns (`notes-backlogs` owns `Notes/Backlogs/`) that this skill writes directly. It is a
mechanical copy, not an authoring task, and **skipping it is how a boundary silently destroys the
answer to "what's left"** — so it belongs here, not in a step someone might not run.

For each area file that had open items, create `Notes/Backlogs/<area-slug>-backlog.md`:

```yaml
---
id: "reporting-backlog"
schema_version: 1
type: "backlog"
title: "Reporting — deferred work"
summary: "Open items carried into <next phase>."
created_at: "<today>"
updated_at: "<today>"
status: "active"
project: "<project>"
initiative: "<NEXT phase's initiative string>"
next_item_id: "<continue the archived file's sequence — never restart at 1>"
companion_docs: ["<the closeout's id>"]
---
```

Then copy the travelling set, as the closeout's *Carried forward* section lists it (L2 defines
what is in it):

- **Keep the original ID.** `R4` stays `R4` forever. A task minted an ID in step 1 keeps it.
- **Add an origin line** — `- **Origin:** R4, Phase 2` — so its lineage survives.
- **Carry the `Status:` line across, normalizing its shape, not only its keyword.** The target
  shape is always `<keyword> — <short note>` — normalize the separator on **every** carried
  item, even one whose keyword was already valid: `blocked, waiting on R4` or
  `blocked waiting on R4` become `blocked — waiting on R4`. The words don't change, only the
  punctuation between them. If the keyword itself was not one of the six, additionally set it
  to `open`, keep a short phrase as the note, and move the full original wording into `Context`
  (`was "known bug, unfixed" in Phase 2 — ...`) so nothing is lost and the keyword is now
  machine-readable.
- **The new file contains only travelling items.** Items whose keyword is `done`, `dropped` or
  `superseded` are left in the archived file — the carried file starts as a clean slate.
- **Item format otherwise follows `notes-backlogs` — check it, don't assume it already does.**
  This is the one point an item gets mechanically rewritten, so it's also the only reliable
  point to catch a field label that has drifted from the current template (most commonly: an
  old label standing in for `Context:`). If a carried item's field names don't match
  `notes-backlogs`' current item format, relabel them during the carry — the content
  moves, only the label changes. Skipping this check is how a drifted label becomes permanent:
  every new item added to the carried file afterwards tends to match its surroundings, not the
  template.

**5c. Write the archive index into `Notes/References/`.** The new phase starts with an empty
`Notes/`, so nothing records what the previous phase produced or decided. Write one document:

`Notes/References/phase-<NN>-archive-index.md`

It answers three questions a new phase actually asks: *what did we document, what did we decide,
and where does any of it sit now.*

**Usually cheap to assemble:** where an archived document carries a `summary:`, its row is that
plus the title — a listing job, not a re-reading job, which is why this runs in light mode too.

**When it is not cheap, say so rather than skipping it.** On a tree that predates this library
(Step 1's no-frontmatter row) there is no `summary:` to list, so each row must be **derived from
the document itself** — a genuine reading job, worth flagging before starting rather than after.
The index is still written: an archive nobody can navigate is what this step exists to prevent,
and the legacy tree is exactly where that matters most.

**Annotate; never copy.** One line per document. The archive holds the content and is immutable —
reproducing any of it here creates a second version that drifts, and nobody will know which is
current.

This file lands in `Notes/References/`, so it carries the same frontmatter every document in that
folder carries — **including `initiative`, which is the NEW phase's string**, the same one step 5b
stamps on the carried backlog. Without it the index is invisible when the *next* boundary runs, and
`project-state-brief`'s machine check reports it as an error ("no frontmatter — invisible to a
phase transition").

```yaml
---
id: "phase-<NN>-archive-index"
schema_version: 1
type: "reference"
title: "Phase <NN> — archive index"
summary: "What Phase <NN> produced and decided, and where each document now sits."
date: "<YYYY-MM-DD>"
status: "active"
superseded_by: null
initiative: "<NEXT phase's initiative string>"
source_paths: ["Archive/Phase_<NN>-<slug>/"]
companion_docs: ["phase-<NN>-closeout"]
---
```

The body annotates the archive section by section: references written, discussions and what each
decided, plans and whether they landed, key decisions, open questions carried forward,
architecture as of this phase, the chronology summaries, and earlier phases.
[EXAMPLE_CLOSEOUT.md](EXAMPLE_CLOSEOUT.md) holds one filled in, for the same fictional phase as
the closeout it shows.

**The references table's *Still relevant* column is the judgment part.** Mark a document relevant where a binding
decision or a carried-forward item depends on it, and superseded where a later document replaced
it. Where you genuinely cannot tell, leave the cell blank rather than guessing — an unfounded
relevance marker sends the next reader to the wrong document with confidence.

**Verify in both directions.** Checking only the closeout against the new backlog is circular:
the closeout is a document this same procedure wrote, so an item omitted there passes silently.

- **Forward** — every ID under *Carried forward* appears in a new backlog file.
- **Backward — read the archived source backlogs directly, never the closeout.** Rebuild the
  travelling set from them, item by item, including the step 1 mints; every ID in it must appear
  in a new backlog file **or** explicitly under the closeout's *Deliberately abandoned*.
- **Open questions — check all three L3 sources, not just `PHASE_CONTEXT.md`.** Every question in
  the archived *Open questions* section, every unresolved *Still open* entry in the archived
  `Discussions/` logs, and every open question in the archived plans must appear in the closeout's
  *Open questions still unanswered* **and** in the archive index. Checking only
  `PHASE_CONTEXT.md` reproduces the single-source failure L3 exists to avoid.

**If any check has a gap, stop and report it by ID or by question.** The backward check is the
one that catches what the forward check is blind to — which is why it must not reuse the forward
check's source.

## Step 6 — Hand off, don't continue  · *light + heavy*

Stop and **ask**, in this order — don't just inform:

> Phase `<NN>` archived to `Archive/Phase_<NN>-<slug>/`. `Notes/` now holds the empty folder
> structure, `<n>` carried-forward backlog items, and an archive index in `Notes/References/`. *(Light mode: `_Summary/` deferred — say so
> here.)* Still missing: `PHASE_CONTEXT.md` and `INHERITED.md`.
>
> 1. *"Want me to run `project-knowledge` now — append this phase to `Project_Timeline.md` and
>    `Key_Decisions.md`?"* Wait for an answer before moving on.
> 2. Once that's answered either way, ask: *"Want me to run `phase-context` now — define the
>    next phase and generate `INHERITED.md`?"*
>
> A "not now" to either is a real answer, not a stall. **No answer at all** leaves the hand-off
> open — and that state is detectable later: no `Notes/PHASE_CONTEXT.md` (`phase-context` never
> ran) *and* the phase absent from `Project_Context/Project_Timeline.md` (`project-knowledge`
> never ran) together mean the hand-off never completed, not that it was declined.

**Do not run those two yourself, and do not treat this hand-off as queued work.**
`project-knowledge` writes to `Project_Context/`, which needs its own instruction from the user,
and defining the next phase's goal, scope and success criteria deserves the user's attention
rather than a paragraph at the tail of a file-moving operation. `project-knowledge` goes first so
`Key_Decisions.md` exists before `INHERITED.md` links to it.

---

## Completing a deferred summary

Triggered by "summarize the Phase 5 archive" or similar, any time after a light transition.
It runs Step 4 against an existing archive — nothing moves, nothing resets, no gates apply.
**It also re-checks Step 5c**, which is light-mode-required but writes into the *current*
`Notes/References/` rather than the archive, so an omission there is invisible when you are
looking at `Archive/`. Full procedure in [HEAVY_MODE.md](HEAVY_MODE.md).

---

## Hard rules

- **Never copy-then-delete.** Move the tree; if impossible, verify byte-for-byte before removing.
- **Never rename folders on the way into the archive.** Relative links depend on the tree
  arriving intact.
- **Never invent the archive folder name.** It comes from `phase_number` + `phase_slug`.
- **Never record an unverified item as delivered.** That error compounds — the next phase builds
  on it.
- **Never restart backlog IDs.** A reused ID makes two different items look like one across the
  boundary.
- **Never silently upgrade to heavy mode.** If the escape hatch suggests it, recommend and let the
  user decide.
- **Report what you could not map.** A transition that silently drops `Files/` is worse than one
  that stops and asks.
