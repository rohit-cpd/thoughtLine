---
name: writing-tests
description: >-
  Use when the user asks to write tests, add test coverage, add a test for a
  function/bug/feature, write a failing test first (TDD), or make sure something
  is tested - and when a recorded output baseline needs turning into a lasting
  characterization test, which is how `refactoring` and
  `research-to-production-port` verify work they cannot specify up front.
  Produces tests that mirror the repo's existing framework and fail for a real
  reason. Not for one-off exploratory checks meant to be read once (see
  `simple-dev-notebook` for Python, `simple-dev-script` for other languages) or
  for deciding where test files live in a new package (see
  `production-grade-implementation` / `production-code-python`) - this skill owns
  how the tests themselves are written.
---

# Writing Tests

When the user wants tests written or added — for new code, existing code, a bug, or a behaviour
that must be preserved — optimize for tests that fail for a real reason and stay meaningful as the
code evolves, not for hitting a coverage percentage. Applies to any language/test framework.

Ordinary test-writing craft — Arrange-Act-Assert, one behaviour per test, naming by expected
outcome, asserting on public behaviour rather than private state — is assumed, not restated here.
What follows is what this library actually depends on.

## Write scope

**Writes test files, and only on an explicit instruction to do so.** Tests are code. If a change
looks untested and nobody asked for tests, say so in one line and move on — offer, don't write.
This includes the safety net `refactoring` needs: when it hands off here because the code it is
about to restructure has no coverage, that hand-off is a request for tests and still needs the
user's go-ahead before anything is written.

Never writes `Notes/`, `Project_Intent/`, `Project_Context/` or `Archive/`. The project's agent
instructions
may narrow this scope; nothing widens it.

## When to use
- User says "write tests", "add test coverage", "test this", "add a regression test", "TDD this",
  or asks you to reproduce a bug with a failing test before fixing it.
- **A recorded output baseline needs to become a real test** — see *Characterization tests* below.
  `refactoring` and `research-to-production-port` both verify by comparing outputs, and both hand
  the lasting version of that check to this skill.
- Not for exploratory "does this work" checks meant to be read once, not kept — that's
  `simple-dev-notebook` for Python, `simple-dev-script` for other languages.
- Not for deciding a new package's file/folder layout — `production-grade-implementation` (or
  `production-code-python` for Python) covers where `tests/` lives and how it mirrors `src/`; this
  skill covers what goes inside those files.

## Match the repo, never introduce a second framework

Find the existing framework and conventions (pytest/unittest/jest/vitest/go test) from existing
test files, a config file (`pytest.ini`, `jest.config.*`), or the dependency manifest — and mirror
it exactly. **Never add a second test framework alongside one already in use.**

If there is no suite at all and the user didn't specify, ask, or default to the language's usual
choice (`pytest` for Python, whatever is already in `package.json` for JS/TS) and say which
default you picked.

## Regression tests: fail first, on purpose

1. Write a test reproducing the reported bug. **Run it and confirm it fails for the right
   reason** — not an import error, not a typo in the fixture.
2. Apply the fix.
3. Confirm it passes, and that it *would* have failed on the old code.

Step 1 is the one that gets skipped, and skipping it produces a test that would have passed before
the fix existed — which proves nothing and will never catch the bug again.

## Characterization tests: locking in behaviour you can't specify

Sometimes the requirement is "whatever it does today, keep doing". Legacy code with no spec, a
refactor's safety net, a port from research code — in all three the correct behaviour is *defined*
by the current output, so there is nothing to assert against except a recorded result.

**Shape:** a committed input fixture, a committed expected-output fixture, and a test that runs the
code on the former and diffs against the latter.

**The rules that make it trustworthy:**

- **Never regenerate the expected output from the code under test.** A test that rewrites its own
  golden file on mismatch passes forever and detects nothing. If a regeneration mode exists, it
  must be an explicit, separate command a human runs deliberately — never a fallback inside the
  test.
- **Commit both fixtures, and keep them small.** The smallest input that exercises the real logic,
  not a whole production run. In this library `research_repository/data/` is gitignored, so a test
  reading a run folder directly passes locally and fails in CI — or worse, passes until someone
  clears their output. Copy what you need into the test tree.
- **Record where the expected output came from** — the run id, commit, or phase — in the test or
  beside the fixture. A baseline nobody can trace is a number nobody can defend.
- **Normalize nondeterminism explicitly, don't loosen the assertion.** Timestamps, dict/map
  ordering, float precision, generated ids: strip or round them in a named step the reader can
  see. Replacing an exact diff with a fuzzy match to make a flaky test pass destroys the only
  thing this test does.
- **Say what it does not cover.** A characterization test pins the paths its fixture exercises and
  nothing else. It is weaker than a test that states intent, and `refactoring` says the same about
  the baseline it builds — don't let a green diff imply full coverage.

**When the golden file legitimately changes:** update it in its own commit, with the reason stated,
and never in the same change as the behaviour that altered it. A golden file updated alongside the
code it guards is a golden file that guarded nothing.

## After writing

- Run the suite. A new test must fail without the fix or feature and pass with it — one that
  passes either way isn't testing anything.
- **Never quietly edit a failing test to make it pass.** If behaviour changed on purpose, say so
  explicitly and change the test as a stated decision. If it changed by accident, you have found a
  bug, not a bad test.
- Don't leave the rest of the suite broken.

## Notes
- If it's ambiguous whether unit, integration, or end-to-end tests are wanted, ask.
- "Production-grade" test suites (fixtures, CI wiring, coverage thresholds) are a bigger ask than
  "add a test for this" — confirm scope if unclear.
- Before writing new test **infrastructure** (a fixture, helper, mock, or parametrization
  scaffold), run `minimal-code-check`'s existence/stdlib/one-line checks on that infrastructure.
  **Not on coverage or thoroughness** — more edge cases and sharper assertions are this skill's
  whole job, not a cost to minimize.
