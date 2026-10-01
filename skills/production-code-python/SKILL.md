---
name: production-code-python
description: 'Use when the user asks for production-ready, reusable, final, robust, or "properly built"/"professional" code for a Python project specifically - explicit words like "production", "robust", "reusable module", "professional". Produces properly modularized Python code (`src/` layout, type hints, `pytest`, structured config) following Python ecosystem conventions concretely, rather than generically. For any other language, use `production-grade-implementation`. Not for moving existing research code into production for the first time — that is a port, and `research-to-production-port` owns it.'
---

# Production Code — Python

Python-tuned sibling to `production-grade-implementation` — same job (a production deliverable,
not a quick exploratory script — see `simple-dev-notebook` for that), with Python's actual
ecosystem conventions spelled out concretely instead of "follow the ecosystem's own convention."
Applies only to Python projects; for any other language, use `production-grade-implementation`,
which stays the general-purpose fallback.

## When to use
- User says "production", "production-ready", "robust", "reusable", "professional", "properly
  built", or asks for something other code/agents will depend on — for a **Python** project.
- Not for prototyping/exploration/debugging — use `simple-dev-notebook`.
- **Not for a non-Python project** — use `production-grade-implementation`.

## Pick a structure (ask if unclear which fits)

**A. Single well-organized module** — best for a small, focused feature where splitting into
multiple files would add indirection without a real benefit.

**B. `src/`-layout package** — best when there are genuinely distinct concerns (data access/I-O,
core business logic, config, an API/CLI entrypoint) that benefit from being separately
testable/reusable.
- `src/<package_name>/` containing `__init__.py`, one or more core-logic modules, a data-access
  module, an entrypoint (`main.py`/CLI/`__main__.py`).
- Mirror the source layout in `tests/` (one test file per source module).
- Prefer the repo's existing layout if one already exists — check before inventing a new one.

## Where production code lives

**Outside `research_repository/`** — in `src/<package_name>/`, the layout `poetry new` and modern
Python packaging tooling produce, or a flat module at the repo root for something small enough not
to need a package at all. Never inside a phase folder, however tempting it is to put the package
next to the notebook it came from. Follow `pyproject.toml` conventions over a bespoke layout: a
local convention competing with the ecosystem's loses, and every new contributor pays for it.

**Do not scaffold a production folder before something real needs it.**

### The research→production boundary

Production never imports from `research_repository/`, a phase folder, or an exploratory script.
**You do not have to be porting anything to break this** — a helper grabbed from a notebook
mid-build does it. In Python the violation usually arrives as:

- `sys.path.append` / `sys.path.insert`, or a `PYTHONPATH` entry reaching into
  `research_repository/`
- `papermill`, `nbconvert` or `runpy` executing a notebook as part of the build or test suite
- a relative import climbing out of the production tree
  (`from ...research_repository import ...`)
- a config value pointing at a model, prompt or CSV under `research_repository/data/`

**None of the last three contain the word `import`, which is why they pass review.**

**The reverse direction is allowed.** A notebook *may* import a production module to exercise or
compare against it — production does not depend on the notebook, so there is no lock-in. The one
caveat: that notebook breaks when production changes, so it must not live in a phase you intend
to freeze.

**Moving an existing notebook or script into production is a port, and
`research-to-production-port` owns it** — which run to port, what the rewrite has to change, how
to verify against that run's recorded output, and the Python-specific detection list in full.
Most ports in this system are exactly this case: a Python notebook becoming Python production
code. Use that skill for the crossing; this one for the shape of what lands.

## Python conventions
- `src/` layout with `pyproject.toml` (Poetry or any PEP 621-compliant build backend) — not a bare
  top-level package unless the project already uses that convention.
- Type hints on public functions/classes; a one-line docstring, not a multi-paragraph one.
- `dataclasses` or `pydantic` models for structured config — never a loose dict passed around.
- The standard library `logging` module (or the project's existing logging setup) — never bare
  `print` in a production code path; `print` is fine only in a thin CLI entrypoint layer, if at
  all.
- Config externalized (env vars, `.env`, a config file loaded once at the entrypoint) — never
  hardcode secrets or environment-specific values inline.

## Error handling & validation
- Handle errors only at system boundaries (I/O, network, external calls, user input) — don't wrap
  logic that can't actually fail.
- Fail loudly with a clear exception rather than silently swallowing errors, unless the caller
  explicitly needs a "best effort, keep going" behavior (state that choice in a comment).

## Testing & verification
- `pytest`, matching the repo's existing framework/style if one already exists.
- See `writing-tests` for how to actually structure and write those tests (naming, assertions,
  mocking boundaries, regression tests for bug fixes).
- If there's no existing test suite and the user didn't ask for tests, at minimum verify the code
  runs/imports cleanly and passes the project's existing lint (`ruff`, `flake8`, or whatever it
  already uses) before considering the task done.

## Notes
- If the user's request is ambiguous between this and a quick/dev version, ask — that's
  `simple-dev-notebook`.
- Before writing new code, run `minimal-code-check`'s laziness checklist first (does it need to
  exist, is it already here, does the standard library or a native feature cover it, can it be one
  line) — "production-grade" governs shape, it isn't permission to skip that check.
- Don't over-engineer: only add structure/abstraction/tests this specific request actually calls
  for — "production-grade" means solid and maintainable, not maximally generic.
- **Three "existing code" cases, three skills.** Already in production and needing cleanup
  without a behaviour change: `refactoring`. Living only in `research_repository/`, tested and
  becoming production for the first time: `research-to-production-port` — a port, not a fresh
  build. Genuinely new production Python: this skill.
