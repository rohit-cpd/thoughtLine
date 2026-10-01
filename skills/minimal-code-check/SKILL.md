---
name: minimal-code-check
description: >-
  Load before writing new code in `production-code-python`,
  `production-grade-implementation`, `research-to-production-port`,
  `simple-dev-notebook`, `simple-dev-script` or `refactoring`, and before writing
  new test infrastructure (fixtures, helpers, mocks) in `writing-tests` - never
  against test coverage itself. Also use directly when the user says "be lazy",
  "lazy mode", "minimal solution", "yagni", "do less", or complains about
  over-engineering, bloat, or unnecessary dependencies. A checklist to run before
  adding code: does it need to exist at all, is something like it already here,
  does the standard library or a native platform feature cover it, does an
  already-installed dependency solve it, can it be one line - write the minimum
  only after those are checked.
---

# Minimal Code Check

Before adding code, check whether less of it — or none — already does the job.

## When this runs

**A skill cannot make another skill run.** This one is loaded — by you, before writing new code —
not triggered automatically by the skills it pairs with. Each of those skills names it in its own
Notes, which is what keeps the pairing self-contained rather than dependent on any project file.

- Before writing new code under `production-code-python`, `production-grade-implementation`,
  `research-to-production-port`, `simple-dev-notebook`, `simple-dev-script` or `refactoring`.
- Before writing new test **infrastructure** in `writing-tests` (fixtures, helpers, mocks) —
  never against test coverage or thoroughness, which is that skill's whole job.
- Directly, when the user says "be lazy", "minimal solution", "yagni", "do less", or complains
  about over-engineering, bloat or unnecessary dependencies.
- **Not** with `document-code-comments` or `git-commit-conventions` — neither writes new logic, so
  the ladder has nothing to check.

## The ladder

Stop at the first rung that holds — but only after actually reading the task and the code it
touches; the ladder shortens the solution, never the reading:

1. **Does this need to exist at all?** Speculative need — skip it, say so in one line. (YAGNI)
2. **Already in this codebase?** A helper, util, type, or pattern that already lives here — reuse
   it before writing a new one.
3. **Does the standard library do it?** Use it.
4. **Does a native platform feature cover it?** A DB constraint over app code, a built-in element
   over a library.
5. **Does an already-installed dependency solve it?** Use it. Never add a new one for what a few
   lines can do.
6. **Can it be one line?** One line.
7. **Only then:** the minimum code that works.

**Bug fix = root cause, not symptom.** Before editing, check every caller of the function being
touched. One guard in the shared function is usually a smaller diff than a guard in every caller
— and patching only the path a report names leaves every sibling caller still broken.

## Rules

- No unrequested abstractions — no interface for one implementation, no config for a value that
  never changes.
- No scaffolding "for later" — later can scaffold for itself.
- Deletion over addition. Fewest files, shortest working diff — once the problem is actually
  understood; the smallest change in the wrong place isn't lazy, it's a second bug.
- Mark a deliberate corner cut with a comment naming the ceiling and the upgrade path:
  `# shortcut: <ceiling> — <upgrade path>` (e.g. `# shortcut: global lock, per-account locks if
  throughput matters`). The marker is deliberately self-explanatory rather than named after this
  skill, so it still reads clearly to someone who has never heard of it.
- Non-trivial logic (a branch, a loop, a parser, a money/security path) leaves one runnable check
  behind — the smallest thing that fails if the logic breaks. Trivial one-liners need none.

## Output

Code first. Then at most three lines: what was skipped, and when to add it back. If the
explanation is longer than the code, cut the explanation — a paragraph defending a simplification
is complexity smuggled back in as prose. An explanation the user explicitly asked for (a report, a
walkthrough) is not this rule's target.

## When NOT to be lazy

Never simplify away: input validation at trust boundaries, error handling that prevents data loss,
security measures, accessibility basics, or anything explicitly requested. If the user insists on
the full version, build it — no re-arguing.

Never skip understanding the problem to ship a smaller diff. Laziness that skips comprehension is
the dangerous kind — it dresses up as efficiency and ships a confident wrong fix. Read fully, then
be lazy.

## Where a paired skill's own rule wins

**`simple-dev-notebook` and `simple-dev-script` both say to prefer duplicating a step over
factoring out a shared helper**, when sharing would hurt top-to-bottom readability. Where that
applies, **their rule wins** — it is tuned for exploratory code, and rung 2 is not a reason to
override it. Rungs 1, 3 and 6 still apply.

**`refactoring`** applies narrowly: its job is restructuring code that already exists, so the
ladder only has something to check when a step introduces genuinely new code — a helper extracted
during a move, for instance — never the restructuring itself.

**"Simplify" splits two ways.** This skill governs code **about to be written**, where there is no
existing behaviour to preserve and the question is whether to write it at all. `refactoring`
restructures code that **already exists**, behaviour held identical against a safety net. A bare
"simplify this" about existing code is `refactoring`'s.
