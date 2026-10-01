---
name: refactoring
description: >-
  Use when the user asks to refactor, clean up, restructure, simplify, or pay
  down tech debt in existing code without changing its behavior - "extract a
  function", "reduce duplication", "this file is a mess, clean it up". Produces
  behavior-preserving changes in small verifiable steps, each one checked against
  a safety net - either a test suite or a recorded output baseline. Not for
  building new features or new production code (see
  `production-grade-implementation` or `production-code-python`), not for one-off
  prototyping (see `simple-dev-notebook` or `simple-dev-script`), and not for
  moving research code into production - that is a port, and
  `research-to-production-port` owns it.
---

# Refactoring

When the user wants existing code restructured — without changing what it does — optimize for
provably unchanged behavior over speed of the rewrite. Applies to any language/codebase.

## When to use
- User says "refactor", "clean this up", "restructure", "simplify this module", "extract a
  function/class", "reduce duplication", "this needs to be cleaner" — about code that already
  exists and already works.
- Not for writing new functionality — `production-grade-implementation`/`production-code-python`
  (final) or `simple-dev-notebook`/`simple-dev-script` (exploratory) cover new code.
- **Not for code crossing out of `research_repository/` into production** — that is
  `research-to-production-port`, where behaviour is *meant* to change in places. Calling it a
  refactor either blocks the work or redefines the word.
- If the user says "refactor" but actually wants different behavior or a new capability, that's a
  feature change, not a refactor — confirm scope before proceeding rather than assuming.

## Prime directive: behavior does not change

Every observable output — return values, side effects, error behavior, public API shape — must be
identical before and after, unless the user explicitly asked for one of those to change (state
that exception plainly if so; it's no longer a pure refactor).

## The safety net: tests **or** a recorded output baseline

Refactoring without a way to detect a behaviour change is just a rewrite with extra risk. **Two
things qualify, and they are not equivalent — take whichever exists, and say which one you used.**

**1. A test suite covering the code being touched.** The stronger net: it states intent, and it
keeps working after this session.

**2. A recorded output baseline.** Run the code on a fixed input *before* the first step and keep
the output. After every step, re-run and diff. Identical output is the check.
- Capture it **before** touching anything. A baseline recorded after the first edit proves nothing.
- It only covers the paths that run actually exercises — weaker than tests, and worth saying so
  rather than treating a green diff as full coverage.
- This is the route `phase-code-carry` hands over on: its Stage 2b establishes exactly this
  baseline by running the carried code, and Stage 3 then tidies against it. **Do not stop and
  demand tests in that situation** — the baseline is the net, and it is already in place.
  `research-to-production-port` verifies the same way, against a run folder's recorded output.

**3. Neither exists → stop and ask.** Say plainly that the code is untested and there is no
reproducible baseline, name what a characterization test would need to cover, and ask for the
go-ahead before writing one. **Writing those tests is itself a code change**, so it needs its own
instruction — then use `writing-tests`. Never silently refactor unprotected code, and never
silently write tests nobody asked for.

Turning a one-off baseline into a test that lasts is `writing-tests`' job — its
*Characterization tests* section — and worth offering once the refactor lands, otherwise the net
disappears when the session does.

## Work in small, verifiable steps

Read the code's actual callers before renaming or moving anything public — a "refactor" that
breaks a caller silently is a bug, not a refactor. Then prefer a sequence of small moves,
re-checking the safety net after **each one**, over a single large rewrite. The mechanics are ordinary — extract, inline, rename, move — and need no
explanation here; what matters is that the net is green between them, so a failure points at the
one step that caused it.

One threshold worth stating, because it is the common mistake: **replace a conditional with
polymorphism or a lookup only when 3+ branches genuinely vary the same way.** Don't introduce a
pattern for two cases. Same threshold as avoiding premature abstraction in new code.

## Keep the diff reviewable

Don't mix a refactor with behavior changes, dependency bumps, or unrelated formatting sweeps — a
reviewer should be able to tell "nothing here changes behavior" at a glance. If a genuine
behavior fix is needed along the way, call it out separately rather than folding it in silently.

## Target style

Only for code **already in production**: if the user wants the result to land on that codebase's
conventions (structure, naming, error handling), use `production-grade-implementation` — or
`production-code-python` for a Python codebase — as the target shape. Go that far only if a full
cleanup was actually requested, not for a narrow, targeted extraction.

## Notes
- If it's ambiguous how deep the refactor should go (one function vs. the whole module), ask.
- **"Simplify" splits two ways.** This skill restructures code that **already exists**, with a
  safety net. If the ask is about code **about to be written** — "keep it minimal", "do less" —
  that is `minimal-code-check`, which has no existing behaviour to preserve.
- If the refactor changed something worth recording — a boundary moved, a decision settled, a
  tracked item closed — say so in one line and let the `notes-*` skills handle it under their own
  rules. This skill does not decide what gets written or when.
- If this refactor writes genuinely new code (a helper introduced during an extraction), run
  `minimal-code-check` on that code. The restructuring mechanics themselves aren't a "does this
  need to exist" question.
