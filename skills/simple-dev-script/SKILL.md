---
name: simple-dev-script
description: 'Use when the user asks for a quick, simple, exploratory, or "dev"/"development" script or small project in a language other than Python - prototyping, debugging data, or wanting to directly see/edit results, without pandas/Jupyter idiom. Produces flat, easy-to-follow scripts with minimal abstraction, either as one self-contained script or as a small pipeline with a simple folder layout. For a Python project, use `simple-dev-notebook` instead - it is tuned to Python''s actual tooling rather than generic advice.'
---

# Simple Dev Script

When the user wants a quick, simple, or exploratory script/small-project in a language **other
than Python** (as opposed to a production deliverable - see `production-grade-implementation`),
optimize for "easy to read top-to-bottom and easy to edit one line at a time," not for reuse or
extensibility. This is the non-Python sibling of `simple-dev-notebook` - the same job, the same
folder conventions, with no pandas/Jupyter idiom baked in. If the language is Python, use that
skill instead; it names concrete tooling this one deliberately doesn't.

## When to use
- User says "simple", "quick", "dev"/"development", "just let me see the data", "prototype",
  "exploration", or similar - for a project in a language other than Python.
- User is frustrated that generated code has too many layers of functions/classes to edit easily.
- **Not for Python** - use `simple-dev-notebook`, which names concrete tools (pandas, Jupyter
  cells) instead of generic advice.
- Not for final deliverables meant to be reused/maintained by others - use
  `production-grade-implementation` (or `production-code-python` for a Python target).

## Pick one structure (ask if unclear which fits)

**A. Single self-contained script** - best when the whole task is one sitting/one flow of work.
- Do not import other local repo modules - everything needed lives in the one file, including
  config as plain variables/constants at the top.
- One file, top to bottom, no handoff to another file.

**B. A small pipeline of scripts** - best when the work has distinct stages someone may want to
re-run independently (e.g. download -> clean -> feature-engineer -> model).
- Each script = one major process/stage, numbered in run order (`1_...`, `2_...`, ...). **The
  number is the contract** for what order they must be run in, so it is not decoration - renumber
  deliberately if a stage is added or dropped.
- **A stage that pulls data itself writes to its own folder, not `data/raw/`.** If `project-start`
  scaffolded this project, `data/raw/` is source data that no stage ever writes to. Give a fresh
  pull its own name (`data/raw_pull/`) instead of reusing it.
- Stage N reads stage N-1's saved output from disk (e.g. a CSV/JSON/parquet in a `data/` folder)
  as its input - do not rely on sharing in-memory state across separate script runs.
- Each script is still internally flat/simple (see "Code style" below) - splitting into stages is
  about the pipeline, not about introducing function/class abstraction within a stage.
- If a small amount of code must be shared across stages, a single flat shared-helpers
  file/module is acceptable - simple single-level functions, not a layered library. **Structure
  C's `common/` test applies here, per stage: share a helper only if changing it *should* change
  every stage's behaviour at once.** A connection or path-resolution helper, yes; a cleaning or
  business-logic function one stage might evolve on its own, no - duplicate it per stage until
  sharing stops being a real option.

**C. A phased research repository** - best when work accumulates in numbered phases, each
exploring an approach that later phases may supersede but must not break. Structure C is
structure B repeated per phase, with one shared output tree.

```
research_repository/
├── README.md                    # index: what each phase was for, which is current
├── common/                      # connections / paths only - see the rule below
├── Phase_01-<slug>/             # CODE ONLY
│   ├── README.md                # what this phase explores, how to run it, what it needs
│   ├── config.<ext>             # this phase's knobs, in one place
│   ├── 1_<step>.<ext>
│   ├── 2_<step>.<ext>
│   ├── utils/                   # phase-local helpers (optional)
│   └── files/                   # phase-specific inputs: prompts, templates
├── Phase_02-<slug>/
└── data/                        # ALL run output, never inside a phase folder
    └── Phase_01-<slug>/
        └── 2026-03-04_14-15-30/ # run id: YYYY-MM-DD_HH-MM-SS
            ├── RUN.md           # what changed going in + the Result once output is reviewed
            ├── config_used.<ext>
            └── output/
```

- **Phase folders hold code only.** Output lives under `research_repository/data/<phase>/<run-id>/`,
  so a phase folder stays small and diffable and every output can be deleted in one sweep. Add
  `research_repository/data/` to `.gitignore` on day one - retrofitting it after a hundred runs
  are already in git history is painful.
- **Run ids are `YYYY-MM-DD_HH-MM-SS`** - uniform, sortable, collision-free. Meaning goes *inside*
  the folder (`RUN.md`), never in its name.
- **Source data that no phase writes lives outside `research_repository/`** entirely, at the
  project's own `data/raw/`. Only run output belongs under `research_repository/data/`.
- **A frozen phase must keep producing what it produced when it was frozen.** That is the test for
  anything shared: put a helper in `common/` only if changing it *should* change every phase's
  behaviour at once. A connection getter, yes. A cleaning function, no - if a later phase cleans
  better, an earlier phase must not silently start cleaning better, or its recorded results stop
  matching its code.
- `common/` does not exist until a **second** phase needs the same helper. Before that,
  duplication costs nothing and the right shape is not yet known.
- The phase folder name matches the phase everywhere else in the project - the same
  `Phase_<NN>-<slug>` used by `Notes/PHASE_CONTEXT.md` and `Archive/`.
- **Starting a phase from the previous phase's code is `phase-code-carry`**, not a manual copy: a
  copied script still points at the old phase's data folder, and running it unchanged writes into
  results a frozen phase depends on.

**Folder layout** (for option B, or any small dev project with multiple files):
top-level numbered scripts for the stages; a small shared-helpers module (connections, one-off
functions), never business logic; `data/` for what passes between stages (`data/raw/`,
`data/processed/`). Subfolders separate distinct concerns, but keep the top level shallow and
obvious - someone should understand the project by listing folders alone.

## Rules for every structure

- **Outputs never live in a code folder.** Even in structure A, write results to a `data/` or
  `runs/` path, not beside the script. This is what lets you clear results without fear.
- **If you will re-run with variations, key the output by run** (`<date>_<time>/`) and record what
  changed. Fixed output paths are fine when you run once and move on - the failure is not
  choosing, then discovering it after overwriting the run you wanted to compare against.
- **Code graduates to a shared helper only when a second script needs it.** Not before, and never
  as a design-first decision.
- **Version suffixes are for parallel variants, not iterations.** `approach_a` / `approach_b` that
  you deliberately compare - fine. `pipeline_v1` through `v6` where each superseded the last is
  git history done by filename, and leaves five dead files you cannot tell apart from the live one.

## `RUN.md` — one per keyed run folder

The loop of a research project is **run → compare → decide**. The run folder already records
*what was tried* (`config_used.<ext>`, `output/`). `RUN.md` records *what was learned* - otherwise
that lives only in someone's head until it maybe surfaces in a meeting weeks later.

Two parts. The **Going in** part is written when the run is set up; the **Result** part when you
have actually looked at the output - the same day, not "later".

```markdown
# <short label for this run>

## Going in
- **Changed vs last run:** e.g. "batch size 32 → 64; everything else held"
- **Comparing against:** `<run-id>`, or "baseline"
- **Expectation:** what you think will happen, one line — so a surprise is visible later

## Result   <!-- `— pending` until the output is reviewed -->
- **Measure:** the one number that decides it — "throughput", "rows dropped", "p95 latency"
- **Outcome:** won | lost | inconclusive vs the comparison run, with the numbers
  ("420 vs 390 req/s — won by 8%")
- **Why:** the cause you believe explains it, one line
- **Keeping:** what carries into the next run as the new baseline
```

**When the Result lands, add a row to the run index** — `notes-references` keeps one undated file
per experiment track (`Notes/References/<track-slug>-experiments.md`) listing every run, what it
changed, its measure and whether it won. It is written automatically, needs no permission, and is
the only thing that answers "what have we already tried". **Keep the losing rows**: they are what
stops an approach being re-tested a month later.

**When a comparison actually settles** — enough runs done to pick an approach — that is also a
`notes-discussions` moment. Starting that topic log needs the user's go-ahead; it cites the
`RUN.md` Result sections of the runs compared, so the decision links to its evidence rather than
restating it.

## Code style (applies to every script regardless of structure)

The same discipline `simple-dev-notebook` applies for Python, translated to whatever your
language's own equivalent tools are - this section names the *principle*, not a specific
call-vocabulary, because that vocabulary genuinely differs by language:

- No function/class abstractions for the actual business logic - flat, imperative, top-to-bottom.
  A tiny one-level helper (e.g. a connection getter) is fine; do not chain helpers that call other
  helpers.
- **One operation per step.** Follow every transformation with a step that inspects the result
  directly, using your language's normal way of doing that - print/log the shape, a sample of
  rows, null/error counts, types. Whatever the equivalent of a REPL, a playground, or an
  interactive shell is for your language, use it the way `simple-dev-notebook` uses a Jupyter
  cell - so results are always visible, never hidden inside a summary object.
- Queries/commands as a plain string assigned to a variable, run directly - no query-builder
  composing other functions. Print or log the query/command itself in its own step so it's
  readable without running it.
- Prefer duplicating similar-looking steps across sections/stages over factoring out a shared
  helper, if sharing would make any single section harder to read top-to-bottom on its own.
- Leave scratch sections between steps if useful for ad-hoc follow-up checks.

## Notes
- **Structure C, the `RUN.md` template and the shared-helper rule are duplicated in
  `simple-dev-notebook`** — deliberately, not by drift. Each skill has to make sense uploaded on its
  own, so a shared bundled file would break on that surface. **Two copies means keeping them in
  sync by hand: change one, change the other.** Only the language-specific parts should differ
  (file extensions, and the per-step inspection vocabulary).
- If the user's request is ambiguous between this and a production build, ask which they want.
- If ambiguous between structures, ask, or default to **A** for one sitting of exploratory work,
  **B** for several distinct stages, and **C** only when the project already works in phases.
- **Nothing under `research_repository/` is ever imported by production code**, and moving code
  across that line is its own operation — `research-to-production-port`, which ports from a named
  run and verifies against its recorded output. **The reverse is fine**: a script may import a
  production module to exercise or compare against it, but it then breaks when production changes,
  so keep it out of any phase you intend to freeze.
- Before writing new code, also run `minimal-code-check`'s laziness checklist - except on the
  reuse/sharing question, where this skill's rule above wins (duplicate until a second script
  needs the helper). Its other rungs still apply.
