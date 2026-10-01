---
name: research-to-production-port
description: >-
  Use when working, tested code in `research_repository/` — a notebook, an exploratory script, a
  phase folder — is becoming production code for the first time: "port this", "productionize
  this", "move this into production", "this works, make it real". The logic already exists, so
  this is a port, not a fresh build: copy it across the boundary, rewrite the research
  assumptions production cannot hold, and verify the result against the winning run's recorded
  output. Not for writing new production code from scratch — that is `production-code-python`
  (Python) or `production-grade-implementation` (any other language). Not for copying code from
  one research phase to the next — that is `phase-code-carry`. Not for restructuring code already
  in production — that is `refactoring`.
---

# Research → Production Port

Moving code across the research/production line is its own operation, with its own failure modes.
It is not a build (the logic already exists and works) and not a refactor (the code is not yet in
production, and behaviour is *meant* to change in places). Skipping it and "just importing the
notebook" is the single most expensive shortcut in this system.

## When to use
- Exploratory code has won its comparison and is becoming the real thing.
- Someone is about to `import` from `research_repository/` — that impulse is this skill's trigger.
- Not for new production code with no research original — `production-code-python` for Python,
  `production-grade-implementation` otherwise.
- Not for carrying code between research phases — `phase-code-carry`.
- Not for code already in production — `refactoring`.

## Write scope

Writes production code and its tests, in whatever tree the project's stack dictates. **Only on an
explicit instruction to port.** If exploratory code looks ready to promote and nobody asked, say
so in one line and move on — offer, don't write.

**Never edits anything under `research_repository/`.** Not to tidy it, not to keep it in sync, not
"while I was in there". The research original is frozen evidence behind its phase's closeout, and
editing it breaks the guarantee that phase depends on. Never writes `Notes/`,
`Project_Intent/`, `Project_Context/` or `Archive/`. The project's agent instructions may narrow
this scope;
nothing widens it.

---

## Step 0 — Establish which run you are porting

**Port a specific run, not "the notebook".** A research folder holds many runs, and they do not
agree with each other — that is what a research folder is *for*. Porting "the current state of the
code" ports whatever the last experiment left behind, which is often not the one that won.

Find, in this order:

1. **The run index** — `Notes/References/<track-slug>-experiments.md`, if the track has one. Its
   *Current best* line and `Outcome` column name the winning run in one read, and its losing rows
   tell you which alternatives were already ruled out, so you do not "improve" the port back into
   something that was tested and lost.
2. **The recorded decision.** When a comparison settles, `notes-discussions` records which
   approach won and on what measure, citing the runs compared. That log names the winning run.
3. **That run's `RUN.md` Result section** — `Measure`, `Outcome`, `Why`, `Keeping`. This is the
   claim the port has to preserve.
4. **That run's `config_used.json`** (or the language's equivalent) — the config **as it was for
   that run**, not `config.py` as it stands now.

State plainly which run id you are porting from. If no recorded decision exists, **stop and ask
which run won** rather than taking the most recent. A port from the wrong run produces production
code whose behaviour traces to no result, and surfaces months later as an unexplainable number.

## Step 1 — The hard boundary: production never imports research code

Never `import` from `research_repository/`, a phase folder, or an exploratory script. The moment
production depends on a prototype, that prototype can never be frozen or changed — you have bought
its bugs permanently, and altering a research notebook becomes a deployment.

**Porting means copying the logic into production code and rewriting it** — not adding a path or
alias that reaches back into research code. The copy is the point: research code and production
code diverge on purpose, because they optimise for different things.

### How to tell it is happening

The violation rarely looks like a violation. Check all of these before treating a module as clean:

- an `import`/`require`/`use` (however the language spells it) naming a phase, notebook, or
  research directory
- **an environment or path-manipulation mechanism reaching into research code** — `sys.path` /
  `PYTHONPATH` in Python, `NODE_PATH` or a bundler alias (webpack/tsconfig `paths`) in JS/TS, a
  `vpath`/`-I` include flag in a C/C++ Makefile, a `replace` directive in Go's `go.mod`
- a relative import/include climbing out of the production tree
- a production config value pointing at a research path — a model file, a prompt file, a CSV
  under `research_repository/data/`
- **a tool that executes a research artifact directly as part of the production build or test
  suite** — the general case is any build or entrypoint script invoking a scratch or prototype
  file

The last two are the ones that slip through review, because neither contains the word `import`.

### Python-specific detection

The same checks in Python's spellings — kept inline, not bundled, because a bundled path breaks
when this skill is uploaded on its own.

- `sys.path.append` / `sys.path.insert`, or a `PYTHONPATH` entry reaching into
  `research_repository/`
- a notebook execution call: `papermill`, `nbconvert` or `runpy` on a research script
- `from ...research_repository import ...` — a relative import climbing out of the tree
- a config value pointing at a model, prompt or CSV under `research_repository/data/`

## Step 2 — What the rewrite actually changes

Porting is not a copy-paste with tidier names. Research code carries assumptions production cannot
hold:

| Research code | Production code |
|---|---|
| Module-level constants at the top of the file | Externalised config — env vars, a config file |
| Assumes one subject, one run, one dataset | Parameterised; concurrent runs must not collide |
| `print` (or the language's equivalent) for everything | The project's logging facility |
| Execution order implied by the artifact's structure (notebook cell order, script top-to-bottom, REPL history) | Explicit calls; no hidden ordering dependency |
| Fails loudly wherever, nowhere handled | Errors handled at system boundaries only |
| Paths relative to the research file's own location | Paths injected, never derived from a source-file-relative guess |
| Global mutable state shared across steps (cells, REPL history, a shared kernel) | Passed arguments and return values |

**The single-subject assumption is usually the largest rewrite and the easiest to miss,** because
the code runs correctly on the one input the researcher used.

For the shape of the result — module layout, error handling, logging, config — follow
`production-code-python` for a Python target or `production-grade-implementation` otherwise. This
skill governs *crossing the line*; those govern what the code looks like once across.

### Config staleness

**Go through the ported config line by line and mark each value a genuine production starting
point or a leftover from that run.** A value tuned for one research run carries across silently
and looks deliberate — a stale value that looks intentional is worse than a missing one.

This is the same check `phase-code-carry` Stage 2a applies when copying between phases, for the
same reason: config is the part of a copy that nothing else verifies.

## Step 3 — Verify the port against recorded output

**Run the ported code on the step 0 run's input and compare against that run's recorded output.**
They must match, or the port changed behaviour and you do not yet know which version is right.

Skipping this means every later difference is ambiguous — a port bug and an intended improvement
look identical.

**Compare against the recorded output files. Never execute the research code to generate a
comparison.** Running the notebook from a production test is itself a boundary violation — it is
the last item in the step 1 checklist — and it makes the production suite depend on a frozen
phase still being runnable. The run folder already contains what you need: `output/` holds the
recorded result, and that is the fixture.

If the outputs cannot match by design (the research version handled one subject, production
handles many), verify on the single-subject case and **say plainly which behaviours were changed
on purpose.**

### Leave the comparison behind as a test

A one-off comparison at port time verifies the port and protects nothing afterwards.

**Copy a small reference input and its expected output into the production tree** — `tests/`, or
wherever the project keeps fixtures — as part of the port. This is required, not optional, because
`research_repository/data/` is gitignored: a test that reads the run folder directly passes on
your machine and fails in CI, or worse, passes until someone clears their run output.

- Keep the fixture **small** — the smallest input that exercises the real logic, not the full run.
- Record in the test, or beside it, **which run id the expected output came from**, so the
  baseline is traceable to the decision that chose it.
- See `writing-tests` → *Characterization tests* for how to write the comparison itself — in
  particular, never let the test regenerate its own expected output.

## Which direction is allowed

**Production importing research: never.**

**Research importing production: allowed, with one caveat.** A notebook importing a production
module to exercise or compare against it creates no lock-in — production does not depend on it.
But it breaks when production changes, so keep it in the current phase rather than one you intend
to freeze.

## What happens to the research original

It stays where it is, frozen, and the two copies diverge from the moment of the port. That is
expected, not drift to be fixed. Record which is authoritative:

- **Production is authoritative for behaviour.** Anything running for real is defined by the code
  in production.
- **The research version is a historical record** of what that phase did, and remains the evidence
  behind that phase's closeout — never edited to "keep it in sync" (see *Write scope*).

## Notes
- Before writing the production code, run `minimal-code-check`'s laziness checklist on it. A port
  is the moment people carry across helpers and abstractions the production version never needs.
- The port is worth recording, and this skill does not record it: a decision about what became
  authoritative belongs in `notes-discussions`, and anything deliberately left in research belongs
  in `notes-backlogs`. Follow those skills' own permission rules.
- If a phase boundary is happening at the same time, these are different operations:
  `phase-transition` archives the notes, `phase-code-carry` copies code to the next research
  phase, and this skill crosses into production. None of them calls the others.
