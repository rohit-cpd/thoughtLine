---
name: production-grade-implementation
description: 'Use when the user asks for production-ready, reusable, final, robust, or "properly built"/"professional" code in a language other than Python - explicit words like "production", "robust", "reusable module", "professional". Produces properly modularized code with single-responsibility functions/classes, following existing repo conventions. For a Python project use `production-code-python` instead, which names Python''s own tooling concretely rather than staying generic. Not for prototyping or exploration: that is `simple-dev-script`, or `simple-dev-notebook` for Python. Not for moving existing research code into production for the first time — that is a port, and `research-to-production-port` owns it.'
---

# Production-Grade Implementation

When the user wants a production deliverable (as opposed to quick exploratory code - see
`simple-dev-script`, or `simple-dev-notebook` for Python), build it with proper software-engineering
structure instead of a flat exploratory script.

**Language scope: everything except Python.** This is the general-purpose build skill, principle-
level so it fits any stack — Go, Rust, TypeScript, Java. **For Python use `production-code-python`
instead**, which does this same job with the ecosystem spelled out concretely (`src/` layout,
`pyproject.toml`, `pytest`, `ruff`); reaching for this one on a Python project gets generic advice
where concrete advice already exists. Otherwise the two are the same skill. Neither owns the
research→production *crossing* — `research-to-production-port` does — but both state the boundary
rule below, because production code can violate it without any port happening.

## When to use
- User says "production", "production-ready", "robust", "reusable", "professional", "properly
  built", or asks for something other code/agents will depend on — **for a non-Python project**.
- **Not for a Python project** - use `production-code-python`.
- Not for prototyping/exploration/debugging - use `simple-dev-script`, or `simple-dev-notebook`
  for Python.

## Pick a structure (ask if unclear which fits)

**A. Single well-organized module/file** - best for a small, focused feature where splitting into
multiple files would add indirection without a real benefit. Keep clear sections/functions inside
the one file rather than one giant block.

**B. Multi-file package** - best when there are genuinely distinct concerns (e.g. data
access/I-O, core business logic, config, an API/CLI entrypoint) that benefit from being separately
testable/reusable.
- Split by responsibility, not by arbitrary size - a config/settings module, a data-access module
  (the I/O boundary), one or more core-logic modules, and an entrypoint (`main`/CLI/handler),
  named however the language conventionally names them.
- Mirror the source layout in `tests/` (one test file per source module) if the repo has/wants
  tests.
- Prefer the repo's existing layout conventions (naming, where config/tests/utils live) over
  introducing a new one - check for an existing pattern first (e.g. how other modules in this repo
  are organized) before inventing a new folder structure.

## Where production code lives

**Outside `research_repository/`, in whatever layout its stack dictates** - `src/`, `backend/`, `frontend/`,
a package root. Follow the ecosystem's own convention (what `poetry new`, `cargo new`,
`create-next-app` or the framework's docs produce) rather than inventing a house layout. A local
convention competing with the ecosystem's loses, and every new contributor pays for it.

**Do not scaffold a production folder before something real needs it.** An empty `src/` signals
intent that does not exist yet.

### The one hard boundary: production never imports from research code

Never `import` from `research_repository/`, a phase folder, or an exploratory script. The moment
production depends on a prototype, that prototype can never be frozen or changed - you have bought
its bugs permanently, and altering a research notebook becomes a deployment.

**How this hides.** You do not have to be porting anything to break this rule - a helper grabbed
from a notebook mid-build does it. Before treating a module as clean, check for:

- an environment or path mechanism reaching into research code: `NODE_PATH` or a bundler alias
  (webpack/tsconfig `paths`), a `replace` directive in Go's `go.mod`, a `vpath`/`-I` include flag,
  `sys.path`/`PYTHONPATH` in Python
- a relative import/include climbing out of the production tree
- a production config value pointing at a research path - a model file, a prompt, a CSV under
  `research_repository/data/`
- a build or entrypoint script executing a research artifact directly

**The last two slip through review, because neither contains the word `import`.**

**The reverse direction is allowed.** Research code *may* import production code - a notebook
exercising or comparing against a production module creates no lock-in, because production does
not depend on the notebook. The one caveat: that notebook breaks when production changes, so it
must not live in a phase you intend to freeze.

**Moving existing research code into production is a port, and `research-to-production-port` owns
it** - which run to port, what the rewrite has to change, and how to verify against recorded
output. Use that skill rather than treating the move as a plain copy, or as an instance of this
one.

This skill covers what the code should look like *once it is across*: the layout, conventions,
error handling and testing below apply to ported and freshly written production code alike.

## Code conventions
- Single-responsibility functions/classes; avoid functions-within-functions call chains that are
  hard to trace - keep the call depth shallow enough that a reader can follow one function call to
  find the real logic.
- Shared abstractions (registries, generic "plug-and-play" processes, base classes, factories) only
  when there are 3+ concrete cases that actually benefit from it, or the user explicitly asks for
  extensibility - otherwise prefer explicit, readable code per case over a premature abstraction.
- Type hints and a one-line docstring on public functions/classes; avoid multi-paragraph docstrings
  where a short one-liner suffices.
- Config/settings centralized and externalized (env vars, `.env`, config file) - never hardcode
  secrets or environment-specific values inline.
- Use the language/repo's logging facility for production code paths instead of bare `print`;
  `print`/inline output is fine only in the thin entrypoint/CLI layer, if at all.

## Error handling & validation
- Handle errors only at system boundaries (I/O, network, external calls, user input) - don't wrap
  logic that can't actually fail, and don't add validation for scenarios that can't occur given the
  caller.
- Fail loudly with a clear message/exception rather than silently swallowing errors, unless the
  caller explicitly needs a "best effort, keep going" behavior (state that choice in a comment).

## Testing & verification
- Add or update unit tests for new/changed core logic if the repo already has a test suite or
  testing convention; match its existing framework/style rather than introducing a new one.
- For how to actually structure and write those tests (naming, assertions, mocking boundaries,
  regression tests for bug fixes), see the `writing-tests` skill.
- If there's no existing test suite and the user didn't ask for tests, at minimum verify the code
  runs/compiles/lints cleanly before considering the task done.

## Notes
- If the user's request is ambiguous between this and a quick/dev version, ask which they want.
- Don't over-engineer: only add structure/abstraction/tests that this specific request actually
  calls for - "production-grade" means solid and maintainable, not maximally generic.
- Before writing new code, run `minimal-code-check`'s laziness checklist first (does it need to exist, is it
  already here, does the standard library or a native feature cover it, can it be one line) -
  "production-grade" governs shape, it isn't permission to skip that check.
- **Two "existing code" cases are not this skill.** Code already in production that must change
  without changing behaviour is `refactoring`. Code that only lives in a notebook or research
  script, tested and becoming production for the first time, is a **port** —
  `research-to-production-port` (see *the one hard boundary* above). Writing genuinely new
  production code is this skill.
