<!--
  TEMPLATE — copy to <project-root>/AGENTS.md and set the title below.

  Three rules here are opinionated defaults, not laws. Read them before adopting:
    • Standing rule 1 — no code changes without an explicit instruction
    • Standing rule 2 — references get written WITHOUT asking you, and any
      discussion log, plan or backlog that already exists gets appended to
    • Standing rule 3 — Notes/ is the only folder writable on an instruction alone

  Rule 2 is the one most likely to surprise you. `notes-references` creates files
  with no prompt, and four of the five skills append to a file that already exists
  without asking. That suits a project where you want the reasoning captured as it
  happens and would rather delete a file than lose a decision. If you would rather
  be asked every time, say so here — per skill and per operation, because the
  Group A table below is split that way.

  Narrowing works; widening does not. Each skill honours an instructions file that
  restricts its write scope and ignores one that tries to grant more, so this
  file can only ever make the library more cautious.

  This file is deliberately short. Each skill states its own write scope, output
  path and frontmatter; repeating them here costs context on every turn.

  Delete this comment once you have read it.
-->

# <Project Name> — Project Instructions

## Standing rules (these govern everything below)

1. **No code changes unless I ask for them.** Analysis, reading and explanation
   are always fine. Writing or editing source files — including comments or
   tests — needs an explicit instruction first.
2. **Documentation is gated per skill, and per operation — see Group A.** Some is
   written without asking; some waits for me. When I do ask, the ask takes any
   form ("document this", "save that", "write it up") — match on what I mean, not
   on a set phrase — and work out **what** to write and **where** it goes rather
   than asking me which skill.
3. **`Notes/` is the only folder you may write to on my instruction alone.**
   `Project_Intent/`, `Project_Context/` and `Archive/` each need their own
   explicit instruction, or you ask me first and wait. "I was already writing
   something" is not authorisation to touch them.
4. **Never delete a document.** `phase-transition` moves files into `Archive/`;
   its documented fallback for environments without `mv` is the only exception,
   and it asks before removing anything.
5. **Don't record an unverified claim as fact** — mark it unverified instead.
6. **Where Group A says "ask me", offer in one line and move on** — *"this needs
   a plan; say the word and I'll write one"* — rather than writing it, or staying
   silent. The reverse also holds: offering instead of doing an automatic write is
   the failure, not the safe option.

Load the skill rather than improvising its format from memory.
**Each skill states its own write scope, output path and frontmatter — this file
does not repeat them.**

## Session start

Run `project-state-brief` once before the first substantive reply. Read-only; it
writes a file only if I ask.

## Group A — documentation

**Creating a file and updating one are separate permissions.**

| Content | Skill | New file | Update existing |
|---|---|---|---|
| Explaining something that already exists | `notes-references` | **Automatic** | **Automatic** |
| What was decided, and why | `notes-discussions` | Ask me | **Automatic** |
| How to build something not yet built | `notes-plans` | Ask me | **Automatic** |
| Work deferred, parked, or just completed | `notes-backlogs` | Ask me | **Automatic** |
| Components, data flow, how pieces connect | `notes-architecture` | Ask me | **Ask me** |

`Discussions/`, `References/` and `Backlogs/` hold **one undated file per topic or
area**, grown over time: past dated entries are immutable, today's is editable, and
a reversal is recorded as a new entry rather than by rewriting the old one.
`Plans/` and `Architecture/` stay dated immutable documents.

Two judgement calls are mine to be asked about: **starting a new discussion log**,
because you cannot tell when a conversation has finished, and **which topic file
something belongs to** when it is genuinely borderline — guessing either buries a
new subject in an unrelated file or splits one subject across two.

Each skill's own *Write scope* section holds the conditions — when its automatic
half fires, and what it must never touch. Two routing rules are this file's, not
theirs:

- **One instruction often warrants more than one file.** Check the others before
  stopping at the first that fits. Write the automatic ones, offer the rest in one
  line, and cross-link via `companion_docs` — which links only files that exist.
  Where a companion was offered and not written, say so in the body of the file
  you did write: deferred work recorded in a recap but tracked nowhere is
  invisible to "what's left".
- **"Document this module" is ambiguous** — a saved write-up
  (`notes-references`), comments in the source (`document-code-comments`, Group
  B), or an answer in chat with no file at all? **Ask, don't default.**
  `document-code-comments` edits source and is governed by rule 1, so it never
  rides along on an automatic write.

If I start something new and no plan or backlog covers it, don't write one
silently and don't skip it either — say it would help, and ask.

## Group B — code: explicit instruction only

Governed by rules 1 and 3. Only on the literal request, never on an inferred
vibe. If it's unclear which applies, **ask** rather than guessing.

`production-grade-implementation` · `production-code-python` · `simple-dev-notebook` ·
`simple-dev-script` · `research-to-production-port` · `refactoring` · `writing-tests` ·
`document-code-comments` · `git-commit-conventions`

Four split along two axes — explore vs. build, and Python vs. any other language:
`simple-dev-notebook` (Python, explore) / `production-code-python` (Python, build)
/ `simple-dev-script` (other, explore) / `production-grade-implementation` (other,
build). Within a language, explore and build are mutually exclusive — if the
request is ambiguous between them, ask; `project-start` settles it once at
initialization. **`research-to-production-port` sits between the columns** in every
language: the logic already exists and works, so it is neither a fresh build nor a
refactor.

Load `minimal-code-check` before writing new code under any of those, and before
writing new test infrastructure in `writing-tests` — never against test coverage.
Its own *When this runs* states the pairing.

**Drafting a commit message is not permission to run the commit.**

**Karpathy discipline** (adapted from `karpathy-guidelines`, MIT —
`multica-ai/andrej-karpathy-skills`), whenever a Group B skill is doing the work:
state assumptions rather than silently picking one reading; write the minimum code
that solves the problem; touch only what the request requires; and turn the task
into a verifiable success criterion before starting.

## Group C — lifecycle: I name these explicitly

`project-start` · `phase-context` · `phase-transition` · `project-knowledge` ·
`phase-code-carry`

These move or rewrite files across the whole project. **A statement that a phase
has ended is not an instruction to archive it.** `phase-transition` runs light by
default, and hands off rather than invoking: run `project-knowledge`, then
`phase-context`, after it finishes.
